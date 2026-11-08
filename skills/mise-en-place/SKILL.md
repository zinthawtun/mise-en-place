---
name: mise-en-place
description: "Spec-driven planning before code. Turns a requirement, PRD, brief or research report into a traceable blueprint (intent, EARS specs with acceptance criteria, architecture and ADRs, roadmap, validation, traceability register) plus coding-agent customisations. Use to kick off or scope a greenfield project or major initiative, adopt spec-driven development on an existing codebase, break a requirements document into specs, design and plan, or add, change or resume scope in a blueprint. Not for implementing backlog items, writing a single ADR, or reviewing an existing design."
argument-hint: "<path to requirement document> [stack] [blueprint folder]"
---

# Mise en place

> *Everything in its place before the heat goes on.* The requirement document is the recipe, specs are the prepped ingredients, the roadmap is the order of cooking, and code is the heat.

Produces a **project blueprint**, the single source of truth for *why*, *what*, *how* and *when*, plus agent customisations that keep later work aligned with it. **Do not use** for implementing backlog items (the generated `spec-driven-implementation` skill), a one-off ADR (the generated `<blueprint>-adr` skill), bug fixes or ordinary documentation.

## Resources
| File | Read when |
|---|---|
| [references/vocabulary.md](./references/vocabulary.md) | **The only file to read before writing.** Every ID format, priority, phase, status, gate value and term. Use its values exactly |
| [references/procedure.md](./references/procedure.md) | Read only the section for the current step, when you reach it |
| [references/templates.md](./references/templates.md) | Read only the template for the file you are about to write |
| [references/customisations.md](./references/customisations.md) | Step 10 only: per-agent paths and merge rules |
| [references/modes.md](./references/modes.md) | Step 1 only, if the mode is `Existing codebase` or `Change` |
| [examples/shortlink/README.md](../../examples/shortlink/README.md) | Optional, if present (plugin or repo install): expected depth and tone. Match its rigour, not its content |
| [scripts/](./scripts/) | Python 3.12+ standard library: [generate_register.py](./scripts/generate_register.py) (steps 5, 9, 11), [check_links.py](./scripts/check_links.py) (step 11) |

Maintainers only: [scripts/test_scripts.py](./scripts/test_scripts.py) and [evals/](../../evals/README.md) (repo only).

## Modes
Choose after the inventory in step 1 and tell the user: `New` runs all steps; `Existing codebase` runs all steps plus [modes.md](./references/modes.md) additions; `Change` follows [modes.md](./references/modes.md) instead of steps 1–8; `Resume` continues from the first incomplete step (see [procedure.md](./references/procedure.md#step-1-intake)).

## Outputs
```text
<blueprint>/            README.md (status) · <source> (never edited) · traceability.md
  00-intent/            intent.md
  01-analysis/          requirement-analysis.md · glossary.md
  02-specs/             README.md · spec-<capability>.md
  03-design/            architecture.md · data-model.md (if data persists) · <interface>-contracts.md · adr/
  04-plan/              roadmap.md · backlog.md
  05-validation/        validation-design.md
  changes/              CR-NNN-*.md (Change mode only)
Per target agent (Copilot, Claude Code, Cursor, AGENTS.md): always-on + path-scoped instructions · 4 project skills · spec-reviewer agent
```

## Procedure
Work layer by layer: read [vocabulary.md](./references/vocabulary.md) first, then read each reference only when you reach the step that needs it, and write each file as soon as its layer is decided. Do not read everything before writing. After every step, update `Mise-en-place step` in the blueprint README. Set gates per [vocabulary.md](./references/vocabulary.md#gates). Use subagents, if available, for independent work: one subagent per capability spec in step 5 (give each the vocabulary, its capability rows and the budget share), and one for the step 11 review. Merge their output yourself and run the scripts once afterwards; without subagents, do the work sequentially. If Python is unavailable, apply the script checks by hand and say so.

| # | Step | Output | Key rule |
|---|---|---|---|
| 1 | Intake | README with status | Read the **whole** source; stop if it is missing or not a requirement; never overwrite customisations |
| 2 | Clarify | Decisions table | **One** round, only unsettled shape-changing questions, each with a default |
| 3 | Analysis | requirement-analysis.md, glossary.md, budget N | Classify every statement; security capability when data, credentials, networks or AI are involved; D-n only if wrong or unsafe without it |
| **A** | Gate A | | Approve capabilities, D-n, risks, OQs. If rejected, revise that layer and re-present; do not start the next step. If the user cannot be reached, proceed on defaults and flag the gate for review ([procedure.md](./references/procedure.md#step-2-clarification)) |
| 4 | Intent | intent.md | Goals with measures; non-goals with rationale |
| 5 | Specs | spec-*.md | EARS, named component, no implementation nouns; ACs for P0–P1 Musts; live ≤ N; OQ defaults never add requirements. Run `generate_register.py --blueprint <blueprint> --budget <N>` |
| **B** | Gate B | | Approve specs against the budget |
| 6 | Design | architecture, data model, contracts, ADRs | Test-enforceable dependency rules; one ADR per hard-to-reverse decision |
| 7 | Plan | roadmap.md, backlog.md | Every phase has an exit criterion; no backlog item before its requirement's phase |
| **C** | Gate C | | Approve ADRs, dependency rules, roadmap |
| 8 | Validation | validation-design.md | Mandatory if the source states a hypothesis |
| 9 | Traceability | traceability.md + register | `generate_register.py --blueprint <blueprint> --budget <N> [--scan src tests]` exits 0 |
| 10 | Customisations | Per target agent | Merge, never overwrite; copy both scripts into the audit skill |
| 11 | Verify | | `check_links.py` 0 broken; register exits 0; if `../../evals/grade.py` exists, run the command in [procedure.md](./references/procedure.md#step-11-verify) and get all PASS |
| 12 | Report | | Mode, files, counts vs budget, defaults accepted, blocking OQs, health commands. **Do not commit unless asked** |

## Rules
- **Never edit the source document** (or a CR's quoted request). Interpretation lives in analysis, specs and ADRs.
- **Measure, then build.** Instrumentation and foundations come before intelligence or automation.
- **Numbers are hypotheses.** Proposed weights and thresholds become `policy:` values with defaults.
- **Unknowns are explicit.** Every unknown is an assumption row or an `OQ-n` with a default.
- **Layers stay separate.** Specs never name products or libraries. Design never introduces behaviour without a requirement.
- **History is append-only.** IDs are never reused; requirements are withdrawn, not deleted; ADRs are superseded or amended, not rewritten; approved analysis rows are resolved, not removed.
- **No code at this stage** unless the user asks.
- **Scale to the source, do not pad.** A one-page brief: about 3 capabilities, 8–20 requirements, 3–5 ADRs. A 50-page report: up to 12 capabilities and 10 ADRs.

## Definition of done
- [ ] Source document unchanged; every substantive source section appears in the breakdown table
- [ ] Every requirement: EARS form, named component, one behaviour, Pri, Phase, Source, Status; no product or library names in specs
- [ ] Live requirements ≤ the recorded budget N (`--budget N` exits 0); no requirement exists only because of an OQ default
- [ ] Every tunable number is a `policy:` value; every unknown is an assumption or an `OQ-n` with a default
- [ ] Security capability present when the system touches data, credentials, networks or AI
- [ ] `generate_register.py` exits 0; `check_links.py` reports 0 broken links
- [ ] Every P0–P1 Must is in the backlog; every phase has an exit criterion
- [ ] Customisations exist for each target agent, with existing content kept verbatim
- [ ] The README status shows step 12, the gate outcomes and every clarification decision
- [ ] Nothing committed unless the user asked
