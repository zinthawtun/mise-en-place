# Worked example: Shortlink

A complete, deliberately small mise-en-place output for a one-page brief. Use it as the quality bar: match the **shape and rigour**, and scale the **volume** to your source.

| Input | Output |
|---|---|
| [blueprint/brief.md](./blueprint/brief.md), about 20 lines, 7 mandates | 3 capabilities · 2 derived · 11 requirements (1 withdrawn), within the 8–20 budget · 8 with ACs · 3 ADRs · 4 phases |

## Judgement calls worth copying
| Where | Call | Why |
|---|---|---|
| [analysis §1](./blueprint/01-analysis/requirement-analysis.md) | "About 6 characters", "under 50 ms" and "a year" became `policy:` values | They are proposals, not mandates |
| [analysis §4](./blueprint/01-analysis/requirement-analysis.md) | D-1 (unknown alias) and D-2 (alias conflict) were derived | The brief implies them but never states them |
| [intent §5](./blueprint/00-intent/intent.md) | NG-2 "no per-user analytics" | Turns a privacy line into an enforceable scope limit |
| [spec-security](./blueprint/02-specs/spec-security.md) | FR-SEC-003 is kept as `Withdrawn`, not deleted | IDs are never reused |
| [spec-redirect](./blueprint/02-specs/spec-redirect.md) | FR-RED-003 is a P2 Must with no AC yet | Allowed: only P0–P1 Musts are gated |
| [roadmap](./blueprint/04-plan/roadmap.md) | P0 is "Measure" with no code | The hypothesis needs a baseline first |
| [ADR-0003](./blueprint/03-design/adr/ADR-0003-auth-on-create-only.md) | Auth on create only, with the trade-off recorded | Hard to reverse; links to the risk it accepts |

## Anti-patterns this example avoids
- "The system shall…": every requirement names a component (Link Service, Redirector).
- Library names in specs: Python and PostgreSQL only appear in design and ADRs.
- Literals in requirements: 50 ms and 6 characters appear only as policy defaults and in AC examples.
- Padding: 3 capabilities and 10 live requirements for a 1-page brief. The baseline measurement is a P0 backlog item, not an FR.

## Try the scripts
```bash
cd examples/shortlink
python3 ../../scripts/generate_register.py --budget 20 --scan tests   # OK, with warnings for Musts that have no AC-named test yet
python3 ../../scripts/check_links.py blueprint .github
```

`.github/` shows the full Copilot output: always-on and path-scoped instructions, the four project skills (with both scripts copied into the audit skill) and the read-only reviewer agent. Other target agents get the same content at the paths in the skill's `references/customisations.md`.
