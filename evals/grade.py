#!/usr/bin/env python3
"""Mechanically grade a mise-en-place output against the skill's Definition of done.

Usage:
  python3 grade.py WORKSPACE [--blueprint blueprint] [--source blueprint/brief.md]
                   [--agents copilot,claude,cursor,agents-md] [--libs python,postgres,...]
                   [--scan src tests] [--budget N] [--frozen src tests]

WORKSPACE should be a git repo committed before the run, so the source document
can be compared with HEAD. Checks that need judgement (EARS quality, sensible
capabilities, report content) are left to a human or model reviewer.
Exit code 0 when every check passes.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
DEFAULT_LIBS = ("python", "postgres", "postgresql", "flask", "django", "fastapi", "react",
                "redis", "kafka", "sqlalchemy", "spring", "express", "dotnet", ".net", "java")
AGENT_FILES = {
    "copilot": [".github/copilot-instructions.md", ".github/instructions", ".github/skills", ".github/agents"],
    "claude": ["CLAUDE.md", ".claude/rules", ".claude/skills", ".claude/agents"],
    "cursor": [".cursor/rules"],
    "agents-md": ["AGENTS.md", ".agents/skills"],
}
AGENT_ALIASES = {"agents": "agents-md", "github": "copilot", "claude-code": "claude"}
LAYERS = ["README.md", "00-intent/intent.md", "01-analysis/requirement-analysis.md",
          "01-analysis/glossary.md", "02-specs/README.md", "03-design/architecture.md",
          "03-design/adr/README.md", "04-plan/roadmap.md", "04-plan/backlog.md",
          "05-validation/validation-design.md", "traceability.md"]


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("workspace")
    ap.add_argument("--blueprint", default="blueprint")
    ap.add_argument("--source", required=True, help="source document path relative to the workspace")
    ap.add_argument("--agents", default="copilot")
    ap.add_argument("--libs", default=",".join(DEFAULT_LIBS))
    ap.add_argument("--scan", nargs="*", default=[])
    ap.add_argument("--budget", type=int, default=0,
                    help="max live requirements (SKILL.md: ~2 x source mandates + derived; 0 = report only)")
    ap.add_argument("--frozen", nargs="*", default=[],
                    help="existing paths that must be unchanged and gain no files (Existing-codebase mode)")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()
    bp = ws / args.blueprint
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    code, out = run(["git", "diff", "--quiet", "HEAD", "--", args.source], ws)
    check("source document unchanged", code == 0, "" if code == 0 else "differs from HEAD")

    for path in args.frozen:
        _, changed = run(["git", "status", "--porcelain", "--untracked-files=all", "--", path], ws)
        check(f"{path} untouched", not changed.strip(), "; ".join(changed.split("\n")[:3]))

    missing = [l for l in LAYERS if not (bp / l).is_file()]
    check("all blueprint layers exist", not missing, ", ".join(missing))

    specs = sorted((bp / "02-specs").glob("spec-*.md"))
    check("at least one spec", specs, f"{len(specs)} specs")
    spec_text = {s.name: s.read_text(encoding="utf-8") for s in specs}

    req_rows = [(n, l) for n, t in spec_text.items() for l in t.splitlines()
                if re.match(r"^\| (FR|NFR)-[A-Z]{2,5}-\d{3} \|", l)]
    system_subj = [f"{n}: {l[:60]}" for n, l in req_rows if re.search(r"\bthe system shall\b", l, re.I)]
    check("no 'the system shall'", not system_subj, "; ".join(system_subj[:3]))

    libs = [x.strip().lower() for x in args.libs.split(",") if x.strip()]
    leaks = []
    for n, l in req_rows:
        for lib in libs:
            if re.search(rf"(?<![\w.]){re.escape(lib)}(?![\w])", l.lower()):
                leaks.append(f"{n}: {lib}")
    check("no technology names in requirements", not leaks, "; ".join(sorted(set(leaks))[:5]))

    live = [l for _, l in req_rows if "withdrawn" not in l.lower()]
    analysis = bp / "01-analysis" / "requirement-analysis.md"
    derived = len(re.findall(r"^\| D-\d+ \|", analysis.read_text(encoding="utf-8"), re.M)) if analysis.is_file() else 0
    budget = args.budget or 0
    check("requirement count within budget", not budget or len(live) <= budget,
          f"{len(live)} live requirements, {derived} derived" + (f", budget {budget}" if budget else ""))

    check("policy values used", any("policy:" in t for t in spec_text.values()))
    check("security capability present",
          any(re.search(r"-SEC-\d{3}", t) for t in spec_text.values()) or (bp / "02-specs" / "spec-security.md").is_file())

    adrs = list((bp / "03-design" / "adr").glob("ADR-*.md"))
    check("ADRs recorded", adrs, f"{len(adrs)} ADRs")

    status = (bp / "README.md").read_text(encoding="utf-8") if (bp / "README.md").is_file() else ""
    m = re.search(r"Mise-en-place step\s*\|\s*(\d+)", status)
    check("README status records step 12", m and m.group(1) == "12", m.group(1) if m else "no step row")

    reg = list(ws.rglob("generate_register.py"))
    reg = [r for r in reg if ".git" not in r.parts]
    check("register script copied into project", reg, ", ".join(str(r.relative_to(ws)) for r in reg))
    code, out = run([sys.executable, str(SCRIPTS / "generate_register.py"), "--blueprint", args.blueprint,
                     "--check", *(["--scan", *args.scan] if args.scan else [])], ws)
    check("register check exits 0 (up to date, no errors)", code == 0, out.strip().splitlines()[-1] if out.strip() else "")

    targets = [args.blueprint] + [p for p in (".github", ".claude", ".cursor", "CLAUDE.md", "AGENTS.md", "README.md")
                                  if (ws / p).exists()]
    code, out = run([sys.executable, str(SCRIPTS / "check_links.py"), *targets], ws)
    check("no broken links", code == 0, out.strip().splitlines()[-1] if out.strip() else "")

    for agent in [a.strip() for a in args.agents.split(",") if a.strip()]:
        agent = AGENT_ALIASES.get(agent, agent)
        if agent not in AGENT_FILES:
            check(f"customisations for {agent}", False, f"unknown agent; use {', '.join(AGENT_FILES)}")
            continue
        miss = [p for p in AGENT_FILES[agent]
                if not ((ws / p).is_file() or ((ws / p).is_dir() and any(f.is_file() for f in (ws / p).rglob("*"))))]
        check(f"customisations for {agent}", not miss, ", ".join(miss))

    width = max(len(r[0]) for r in results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name.ljust(width)}  {detail}")
    passed = sum(ok for _, ok, _ in results)
    print(f"Score: {passed}/{len(results)}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
