#!/usr/bin/env python3
"""Regenerate and audit the requirement register in <blueprint>/traceability.md.

Usage:
  python3 generate_register.py [--blueprint blueprint] [--root .]
                               [--ac-phases P0,P1] [--scan src tests ...] [--check]
                               [--budget N]

Checks (errors fail the run with exit code 1):
  - duplicate requirement IDs
  - Must requirements without acceptance criteria in the gated phases (--ac-phases)
  - backlog items that reference unknown IDs, or that are scheduled before the
    phase of the requirement they satisfy
  - ACs that declare `Needs: FR-…` for a requirement that is unknown or scheduled in a later phase
  - code/tests (--scan) that reference unknown or Withdrawn requirement/AC IDs
  - with --check: the register in traceability.md is out of date (nothing is written)
Warnings (reported, never fail): FRs without a phase, requirements with more than one
"shall", backlog items that satisfy no requirement or hypothesis, gated Musts with no backlog
item, gated Musts whose ACs are not referenced by any scanned file, scanned files skipped
as too large or not UTF-8, scan paths that do not exist.
If traceability.md does not exist yet (before step 9), the audit still runs and
nothing is written. Writing regenerates everything from the register marker up to the next
heading; text after that heading is kept. Exit code 2 means a usage or input error:
02-specs/ is missing, traceability.md lacks the register marker (or has it more than once),
--ac-phases or --budget is invalid, or a file cannot be read as UTF-8 text.
Requirement table columns: | ID | Requirement | Pri | Phase | Source | Status? |
(Status is optional; "Withdrawn" in the Status or Requirement cell retires the row).
"""

import argparse
import os
import re
import shutil
import sys
import tempfile
from collections import Counter
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Optional, TypedDict

MARKER = "## 3. Requirement register"
REGISTER_SECTION = re.compile(r"^" + re.escape(MARKER) + r"[ \t]*$.*?(?=^#{1,6} |\Z)", re.M | re.S)
ROW = re.compile(r"^\| ((FR|NFR)-([A-Z]{2,5})-(\d{3})) \| (.*)$", re.M)
FRONT_PHASE = re.compile(r"^phase:\s*(P\d+)\s*$", re.M)
REQ_REF = re.compile(r"\b((?:FR|NFR)-[A-Z]{2,5}-\d{3})\b")
HYP_REF = re.compile(r"\bH-\d+\b")
# Matches AC-RED-001.1 in docs and test_AC_RED_001_1 in test names (no \b: "_" is a word char).
AC_REF = re.compile(r"(?<![A-Za-z0-9])AC[-_](NFR[-_])?([A-Z]{2,5})[-_](\d{3})[-_.](\d+)")
BACKLOG_ROW = re.compile(r"^\| ([A-Z][A-Z0-9]*-(\d+)-\d{2}) \|(.*)$", re.M)
SKIP_DIRS = {".git", "node_modules", "bin", "obj", "dist", "build", "target",
             ".venv", "venv", "__pycache__", ".idea", ".vs", "coverage"}
MAX_SCAN_BYTES = 1_000_000
SHALL = re.compile(r"\bshall\b", re.I)


class Requirement(TypedDict):
    id: str
    kind: str
    pri: str
    phase: str
    spec: str
    ac: bool
    compound: bool
    withdrawn: bool
    status: str


class InputError(Exception):
    pass


FR_AC = re.compile(r"AC-([A-Z]{2,5}-\d{3})\.\d")
NFR_AC = re.compile(r"AC-NFR-([A-Z]{2,5}-\d{3})\.\d|\*\*NFR-([A-Z]{2,5}-\d{3}) AC\*\*")


def ac_keys(text: str) -> dict[str, set[str]]:
    """Requirement keys (e.g. RED-001) that have at least one AC in the text, by kind."""
    return {
        "FR": set(FR_AC.findall(text)),
        "NFR": {a or b for a, b in NFR_AC.findall(text)},
    }


def phase_num(phase: Optional[str]) -> Optional[int]:
    if phase is None or not re.fullmatch(r"P\d+", phase):
        return None
    return int(phase[1:])


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        raise InputError(f"{path} is not valid UTF-8: {e.reason}") from e


def load_requirements(specs: Path) -> list[Requirement]:
    rows: list[Requirement] = []
    for spec in sorted(specs.glob("spec-*.md")):
        text = read_utf8(spec)
        fm = FRONT_PHASE.search(text.split("\n---", 2)[0] if text.startswith("---") else "")
        spec_phase = fm.group(1) if fm else "—"
        acs = ac_keys(text)
        for m in ROW.finditer(text):
            rid, kind, prefix, num, rest = m.groups()
            cells = [c.strip() for c in rest.split("|")]
            pri = cells[1] if len(cells) > 1 else ""
            if kind == "FR":
                phase = cells[2] if len(cells) > 2 and phase_num(cells[2]) is not None else "—"
            else:
                phase = spec_phase
            if kind == "FR" and len(cells) > 4:
                status = cells[4]
            elif kind == "NFR" and len(cells) > 2:
                status = cells[2]
            else:
                status = ""
            withdrawn = "withdrawn" in (cells[0] + " " + status).lower()
            rows.append({
                "id": rid, "kind": kind, "pri": pri, "phase": phase, "spec": spec.name,
                "ac": f"{prefix}-{num}" in acs[kind],
                "compound": len(SHALL.findall(cells[0] if cells else "")) > 1,
                "withdrawn": withdrawn,
                "status": "Withdrawn" if withdrawn else (status or "—"),
            })
    return rows


AC_LINE = re.compile(r"^[\s>*|-]*\**AC-(NFR-)?([A-Z]{2,5})-(\d{3})\.\d+", re.M)
NEEDS = re.compile(r"Needs:\s*([^\n]*)")


def audit_ac_needs(specs: Path, by_id: dict[str, Requirement]) -> list[str]:
    """An AC may list `Needs: FR-…` for other requirements it relies on.

    They must exist and must not be scheduled in a later phase than the AC's own requirement.
    """
    errors: list[str] = []
    for spec in sorted(specs.glob("spec-*.md")):
        for line in read_utf8(spec).splitlines():
            m = AC_LINE.match(line)
            n = NEEDS.search(line)
            if not m or not n:
                continue
            own = by_id.get(f"{'NFR' if m.group(1) else 'FR'}-{m.group(2)}-{m.group(3)}")
            own_phase = phase_num(own["phase"]) if own else None
            for rid in REQ_REF.findall(n.group(1)):
                dep = by_id.get(rid)
                if dep is None:
                    errors.append(f"AC in {spec.name} needs unknown {rid}")
                    continue
                dep_phase = phase_num(dep["phase"])
                if own and own_phase is not None and dep_phase is not None and dep_phase > own_phase:
                    errors.append(f"AC of {own['id']} ({own['phase']}) needs {rid} scheduled for {dep['phase']}")
    return errors


def render_register(rows: list[Requirement]) -> str:
    intro = (
        f"{MARKER}\n\n"
        "AC ✓ means at least one Given/When/Then acceptance criterion exists. "
        "**Must** requirements without ✓ need one before they can move from `Draft` to `Agreed`.\n\n"
        "| ID | Pri | Phase | Status | Spec | AC |\n|---|---|---|---|---|---|\n"
    )
    body = "".join(
        f"| {r['id']} | {r['pri']} | {r['phase']} | {r['status']} | [{r['spec']}](./02-specs/{r['spec']}) | "
        f"{'' if r['withdrawn'] else ('✓' if r['ac'] else '')} |\n"
        for r in rows
    )
    return intro + body


def splice_register(trace: str, rows: list[Requirement]) -> str:
    """Regenerate the register section; headings after it are kept."""
    m = REGISTER_SECTION.search(trace)
    if m is None:
        raise InputError(f"no '{MARKER}' heading to replace")
    head, tail = trace[:m.start()], trace[m.end():]
    return head + render_register(rows) + ("\n" if tail else "") + tail


def write_atomic(path: Path, text: str) -> None:
    """Write via a temp file so an interrupted run cannot truncate the register."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        if path.exists():
            shutil.copymode(path, tmp)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def audit_backlog(backlog: Path, by_id: dict[str, Requirement]) -> tuple[list[str], list[str], set[str], bool]:
    errors: list[str] = []
    warnings: list[str] = []
    covered: set[str] = set()
    if not backlog.is_file():
        return errors, warnings, covered, False
    for m in BACKLOG_ROW.finditer(read_utf8(backlog)):
        item, item_phase, rest = m.group(1), int(m.group(2)), m.group(3)
        if not REQ_REF.search(rest) and not HYP_REF.search(rest):
            warnings.append(f"backlog item satisfies no requirement or hypothesis (project activity?): {item}")
        for rid in REQ_REF.findall(rest):
            req = by_id.get(rid)
            if req is None:
                errors.append(f"backlog {item} references unknown {rid}")
                continue
            covered.add(rid)
            if not req["withdrawn"] and not req["ac"]:
                warnings.append(
                    f"backlog {item} satisfies {rid} but it has no AC (a 'Done when' must name existing ACs)")
            rp = phase_num(req["phase"])
            if rp is not None and item_phase < rp:
                errors.append(f"backlog {item} (P{item_phase}) satisfies {rid} scheduled for {req['phase']}")
    return errors, warnings, covered, True


def iter_scan_files(paths: Iterable[str], exclude: Path) -> Iterator[Path]:
    for p in paths:
        base = Path(p).resolve()
        for f in (base.rglob("*") if base.is_dir() else [base]):
            if not f.is_file() or exclude in f.parents:
                continue
            # Match skip dirs relative to the scan root, not the absolute path.
            rel_dirs = f.relative_to(base).parts[:-1] if base.is_dir() else ()
            if any(part in SKIP_DIRS for part in rel_dirs):
                continue
            yield f


def audit_code(
    paths: Iterable[str], exclude: Path, by_id: dict[str, Requirement]
) -> tuple[list[str], list[str], set[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ac_seen: set[str] = set()
    for f in iter_scan_files(paths, exclude):
        try:
            if f.stat().st_size > MAX_SCAN_BYTES:
                warnings.append(f"{f}: not scanned, larger than {MAX_SCAN_BYTES} bytes")
                continue
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            warnings.append(f"{f}: not scanned, not UTF-8 text")
            continue
        except OSError as e:
            warnings.append(f"{f}: not scanned, {e.strerror or e}")
            continue
        refs = set(REQ_REF.findall(text))
        for nfr, prefix, num, _ in AC_REF.findall(text):
            rid = f"{'NFR' if nfr else 'FR'}-{prefix}-{num}"
            refs.add(rid)
            ac_seen.add(rid)
        for rid in sorted(refs):
            req = by_id.get(rid)
            if req is None:
                errors.append(f"{f}: references unknown {rid}")
            elif req["withdrawn"]:
                errors.append(f"{f}: references Withdrawn {rid}")
    return errors, warnings, ac_seen


def nonneg_int(value: str) -> int:
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a whole number, got {value!r}") from None
    if n < 0:
        raise argparse.ArgumentTypeError("must be 0 or more")
    return n


def phase_list(value: str) -> set[str]:
    phases = {p.strip() for p in value.split(",") if p.strip()}
    bad = sorted(p for p in phases if phase_num(p) is None)
    if bad:
        raise argparse.ArgumentTypeError(f"not a phase (expected P0, P1, ...): {', '.join(bad)}")
    return phases


def run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    blueprint = (root / args.blueprint).resolve()
    specs, trace_path = blueprint / "02-specs", blueprint / "traceability.md"
    if not specs.is_dir():
        print(f"Expected {specs}/", file=sys.stderr)
        return 2
    trace = read_utf8(trace_path) if trace_path.is_file() else None
    if trace is not None:
        found = len(REGISTER_SECTION.findall(trace))
        if found != 1:
            print(f"Expected one '{MARKER}' heading in {trace_path}, found {found}", file=sys.stderr)
            return 2

    rows = load_requirements(specs)
    by_id = {r["id"]: r for r in rows}
    gated = args.ac_phases
    errors, warnings = [], []
    warnings += [f"scan path not found, not scanned: {s}" for s in args.scan if not Path(s).exists()]

    if trace is None:
        if args.check:
            errors.append(f"{trace_path} does not exist")
        else:
            warnings.append(f"{trace_path.name} not found: audit only, register not written (normal before step 9)")
    elif args.check:
        if splice_register(trace, rows) != trace:
            errors.append(f"register in {trace_path} is out of date; rerun without --check")
    else:
        write_atomic(trace_path, splice_register(trace, rows))

    dupes = sorted(i for i, c in Counter(r["id"] for r in rows).items() if c > 1)
    errors += [f"duplicate ID {d}" for d in dupes]

    live = [r for r in rows if not r["withdrawn"]]
    gated_musts = [r for r in live if r["pri"] == "M" and r["phase"] in gated]
    errors += [f"Must without AC: {r['id']} ({r['phase']}, {r['spec']})" for r in gated_musts if not r["ac"]]
    if args.budget and len(live) > args.budget:
        errors.append(f"requirement budget exceeded: {len(live)} live > {args.budget}; merge or demote to OQ-n")
    later = [r for r in live if r["pri"] == "M" and not r["ac"] and r["phase"] not in gated]
    warnings += [f"FR without phase: {r['id']}" for r in live if r["kind"] == "FR" and r["phase"] == "—"]

    b_errors, b_warnings, covered, has_backlog = audit_backlog(blueprint / "04-plan" / "backlog.md", by_id)
    errors += b_errors
    warnings += b_warnings
    errors += audit_ac_needs(specs, by_id)
    warnings += [f"requirement has more than one 'shall' (split it): {r['id']}" for r in live if r["compound"]]
    if has_backlog:
        warnings += [f"gated Must not in backlog: {r['id']}" for r in gated_musts if r["id"] not in covered]

    if args.scan:
        c_errors, c_warnings, ac_seen = audit_code(args.scan, blueprint, by_id)
        errors += c_errors
        warnings += c_warnings
        warnings += [f"gated Must with no AC-named test: {r['id']}" for r in gated_musts if r["id"] not in ac_seen]

    print(f"Requirements: {len(rows)}  (with AC: {sum(r['ac'] for r in rows)}, withdrawn: {len(rows) - len(live)})")
    print(f"Live requirements: {len(live)}  (budget: {args.budget or 'not set'})")
    print(f"Gated phases: {', '.join(sorted(gated)) or 'none'}  gated Musts: {len(gated_musts)}")
    print(f"Later-phase Musts without AC (allowed while Draft): {len(later)}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"Result: {'FAIL' if errors else 'OK'} ({len(errors)} errors, {len(warnings)} warnings)")
    return 1 if errors else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--blueprint", default="blueprint", help="blueprint folder name (default: blueprint)")
    ap.add_argument("--root", default=".", help="repository root (default: cwd)")
    ap.add_argument("--ac-phases", type=phase_list, default="P0,P1",
                    help="phases whose Musts must have ACs (default: P0,P1; empty to disable)")
    ap.add_argument("--scan", nargs="*", default=[], metavar="PATH",
                    help="code/test paths to scan for requirement and AC IDs")
    ap.add_argument("--check", action="store_true",
                    help="do not write; fail if the register is out of date (for CI)")
    ap.add_argument("--budget", type=nonneg_int, default=0,
                    help="fail if live (non-withdrawn) requirements exceed N (0 = report only)")
    args = ap.parse_args()
    try:
        return run(args)
    except (OSError, InputError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
