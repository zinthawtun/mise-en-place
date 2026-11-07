#!/usr/bin/env python3
"""Regenerate and audit the requirement register in <blueprint>/traceability.md.

Usage:
  python3 generate_register.py [--blueprint blueprint] [--root .]
                               [--ac-phases P0,P1] [--scan src tests ...] [--check]

Checks (errors fail the run with exit code 1):
  - duplicate requirement IDs
  - Must requirements without acceptance criteria in the gated phases (--ac-phases)
  - backlog items that reference unknown IDs, or that are scheduled before the
    phase of the requirement they satisfy
  - ACs that declare `Needs: FR-…` for a requirement that is unknown or scheduled in a later phase
  - code/tests (--scan) that reference unknown or Withdrawn requirement/AC IDs
  - with --check: the register in traceability.md is out of date (nothing is written)
Warnings (reported, never fail): FRs without a phase, requirements with more than one
"shall", backlog items that satisfy no requirement, gated Musts with no backlog
item, gated Musts whose ACs are not referenced by any scanned file.
If traceability.md does not exist yet (before step 9), the audit still runs and
nothing is written. Exit code 2 means 02-specs/ is missing, or traceability.md
exists without the register marker.
Requirement table columns: | ID | Requirement | Pri | Phase | Source | Status? |
(Status is optional; "Withdrawn" in the Status or Requirement cell retires the row).
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

MARKER = "## 3. Requirement register"
ROW = re.compile(r"^\| ((FR|NFR)-([A-Z]{2,5})-(\d{3})) \| (.*)$", re.M)
FRONT_PHASE = re.compile(r"^phase:\s*(P\d+)\s*$", re.M)
REQ_REF = re.compile(r"\b((?:FR|NFR)-[A-Z]{2,5}-\d{3})\b")
# Matches AC-RED-001.1 in docs and test_AC_RED_001_1 in test names (no \b: "_" is a word char).
AC_REF = re.compile(r"(?<![A-Za-z0-9])AC[-_](NFR[-_])?([A-Z]{2,5})[-_](\d{3})[-_.](\d+)")
BACKLOG_ROW = re.compile(r"^\| ([A-Z][A-Z0-9]*-(\d+)-\d{2}) \|(.*)$", re.M)
SKIP_DIRS = {".git", "node_modules", "bin", "obj", "dist", "build", "target",
             ".venv", "venv", "__pycache__", ".idea", ".vs", "coverage"}
MAX_SCAN_BYTES = 1_000_000


def has_ac(text: str, kind: str, key: str) -> bool:
    if kind == "FR":
        return re.search(rf"AC-{key}\.\d", text) is not None
    return re.search(rf"AC-NFR-{key}\.\d|\*\*NFR-{key} AC\*\*", text) is not None


def phase_num(phase: str):
    return int(phase[1:]) if re.fullmatch(r"P\d+", phase or "") else None


def load_requirements(specs: Path):
    rows = []
    for spec in sorted(specs.glob("spec-*.md")):
        text = spec.read_text(encoding="utf-8")
        fm = FRONT_PHASE.search(text.split("\n---", 2)[0] if text.startswith("---") else "")
        spec_phase = fm.group(1) if fm else "—"
        for m in ROW.finditer(text):
            rid, kind, prefix, num, rest = m.groups()
            cells = [c.strip() for c in rest.split("|")]
            pri = cells[1] if len(cells) > 1 else ""
            if kind == "FR":
                phase = cells[2] if len(cells) > 2 and phase_num(cells[2]) is not None else "—"
            else:
                phase = spec_phase
            status = cells[4] if kind == "FR" and len(cells) > 4 else (cells[2] if kind == "NFR" and len(cells) > 2 else "")
            withdrawn = "withdrawn" in (cells[0] + " " + status).lower()
            rows.append({
                "id": rid, "kind": kind, "pri": pri, "phase": phase, "spec": spec.name,
                "ac": has_ac(text, kind, f"{prefix}-{num}"),
                "compound": len(re.findall(r"\bshall\b", cells[0] if cells else "", re.I)) > 1,
                "withdrawn": withdrawn,
                "status": "Withdrawn" if withdrawn else (status or "—"),
            })
    return rows


AC_LINE = re.compile(r"^[\s>*|-]*\**AC-(NFR-)?([A-Z]{2,5})-(\d{3})\.\d+", re.M)
NEEDS = re.compile(r"Needs:\s*([^\n]*)")


def audit_ac_needs(specs: Path, by_id):
    """An AC may list `Needs: FR-…` for other requirements it relies on; they must exist and not be later-phase."""
    errors = []
    for spec in sorted(specs.glob("spec-*.md")):
        for line in spec.read_text(encoding="utf-8").splitlines():
            m = AC_LINE.match(line)
            n = NEEDS.search(line)
            if not m or not n:
                continue
            own = by_id.get(f"{'NFR' if m.group(1) else 'FR'}-{m.group(2)}-{m.group(3)}")
            for rid in REQ_REF.findall(n.group(1)):
                dep = by_id.get(rid)
                if dep is None:
                    errors.append(f"AC in {spec.name} needs unknown {rid}")
                elif own and phase_num(own["phase"]) is not None and phase_num(dep["phase"]) is not None \
                        and phase_num(dep["phase"]) > phase_num(own["phase"]):
                    errors.append(f"AC of {own['id']} ({own['phase']}) needs {rid} scheduled for {dep['phase']}")
    return errors


def render_register(rows) -> str:
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


NO_REQ: list = []
NO_AC: list = []


def audit_backlog(backlog: Path, by_id):
    errors, covered = [], set()
    if not backlog.is_file():
        return errors, covered, False
    for m in BACKLOG_ROW.finditer(backlog.read_text(encoding="utf-8")):
        item, item_phase, rest = m.group(1), int(m.group(2)), m.group(3)
        if not REQ_REF.search(rest):
            NO_REQ.append(item)
        for rid in REQ_REF.findall(rest):
            req = by_id.get(rid)
            if req is None:
                errors.append(f"backlog {item} references unknown {rid}")
                continue
            covered.add(rid)
            if not req["withdrawn"] and not req["ac"]:
                NO_AC.append(f"{item} satisfies {rid}")
            rp = phase_num(req["phase"])
            if rp is not None and item_phase < rp:
                errors.append(f"backlog {item} (P{item_phase}) satisfies {rid} scheduled for {req['phase']}")
    return errors, covered, True


def iter_scan_files(paths, exclude: Path):
    for p in paths:
        p = Path(p).resolve()
        if p.is_file():
            yield p
            continue
        for f in p.rglob("*"):
            if not f.is_file() or f.stat().st_size > MAX_SCAN_BYTES:
                continue
            if any(part in SKIP_DIRS for part in f.parts) or exclude in f.parents:
                continue
            yield f


def audit_code(paths, exclude: Path, by_id):
    errors, ac_seen = [], set()
    for f in iter_scan_files(paths, exclude):
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
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
    return errors, ac_seen


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--blueprint", default="blueprint", help="blueprint folder name (default: blueprint)")
    ap.add_argument("--root", default=".", help="repository root (default: cwd)")
    ap.add_argument("--ac-phases", default="P0,P1",
                    help="phases whose Musts must have ACs (default: P0,P1; empty to disable)")
    ap.add_argument("--scan", nargs="*", default=[], metavar="PATH",
                    help="code/test paths to scan for requirement and AC IDs")
    ap.add_argument("--check", action="store_true",
                    help="do not write; fail if the register is out of date (for CI)")
    ap.add_argument("--budget", type=int, default=0,
                    help="fail if live (non-withdrawn) requirements exceed N (0 = report only)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    blueprint = root / args.blueprint
    specs, trace_path = blueprint / "02-specs", blueprint / "traceability.md"
    if not specs.is_dir():
        print(f"Expected {specs}/", file=sys.stderr)
        return 2
    trace = trace_path.read_text(encoding="utf-8") if trace_path.is_file() else None
    if trace is not None and MARKER not in trace:
        print(f"Marker '{MARKER}' not found in {trace_path}", file=sys.stderr)
        return 2

    rows = load_requirements(specs)
    by_id = {r["id"]: r for r in rows}
    gated = {p.strip() for p in args.ac_phases.split(",") if p.strip()}
    errors, warnings = [], []

    if trace is None:
        if args.check:
            errors.append(f"{trace_path} does not exist")
        else:
            warnings.append(f"{trace_path.name} not found: audit only, register not written (normal before step 9)")
    elif args.check:
        new_trace = trace.split(MARKER)[0] + render_register(rows)
        if new_trace != trace:
            errors.append(f"register in {trace_path} is out of date; rerun without --check")
    else:
        trace_path.write_text(trace.split(MARKER)[0] + render_register(rows), encoding="utf-8")

    dupes = sorted(i for i, c in Counter(r["id"] for r in rows).items() if c > 1)
    errors += [f"duplicate ID {d}" for d in dupes]

    live = [r for r in rows if not r["withdrawn"]]
    gated_musts = [r for r in live if r["pri"] == "M" and r["phase"] in gated]
    errors += [f"Must without AC: {r['id']} ({r['phase']}, {r['spec']})" for r in gated_musts if not r["ac"]]
    if args.budget and len(live) > args.budget:
        errors.append(f"requirement budget exceeded: {len(live)} live > {args.budget}; merge or demote to OQ-n")
    later = [r for r in live if r["pri"] == "M" and not r["ac"] and r["phase"] not in gated]
    warnings += [f"FR without phase: {r['id']}" for r in live if r["kind"] == "FR" and r["phase"] == "—"]

    b_errors, covered, has_backlog = audit_backlog(blueprint / "04-plan" / "backlog.md", by_id)
    errors += b_errors
    errors += audit_ac_needs(specs, by_id)
    warnings += [f"backlog {i} but it has no AC (a 'Done when' must name existing ACs)" for i in NO_AC]
    warnings += [f"backlog item satisfies no requirement (project activity?): {i}" for i in NO_REQ]
    warnings += [f"requirement has more than one 'shall' (split it): {r['id']}" for r in live if r["compound"]]
    if has_backlog:
        warnings += [f"gated Must not in backlog: {r['id']}" for r in gated_musts if r["id"] not in covered]

    if args.scan:
        c_errors, ac_seen = audit_code(args.scan, blueprint, by_id)
        errors += c_errors
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


if __name__ == "__main__":
    sys.exit(main())
