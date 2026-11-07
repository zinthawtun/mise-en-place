# Mise en place: controlled vocabulary

Use these terms and values **exactly** as written. Do not invent synonyms. Every other file in the skill refers here.

## Dates
Every date is written `DD-MM-YYYY` (for example, `07-11-2026`). Never use another format.

## Modes
| Value | When |
|---|---|
| `New` | No blueprint exists and there is little or no code |
| `Existing codebase` | Code exists but there is no blueprint |
| `Change` | A blueprint exists with step 12 done, and the user adds, changes or removes scope |
| `Resume` | A blueprint exists, and its README shows `Mise-en-place step` below 12 |

## Identifiers
| Kind | Format | Example | Rule |
|---|---|---|---|
| Capability prefix | 3 uppercase letters | `LED`, `MEM`, `SEC` | One per capability |
| Functional requirement | `FR-<PREFIX>-<NNN>` | `FR-LNK-001` | Never reused or renumbered |
| Non-functional requirement | `NFR-<PREFIX>-<NNN>` | `NFR-RED-001` | Never reused or renumbered |
| Acceptance criterion | `AC-<PREFIX>-<NNN>.<n>` | `AC-LNK-001.1` | For an NFR: `AC-NFR-<PREFIX>-<NNN>.<n>` |
| Derived requirement | `D-n` | `D-1` | In the analysis only |
| Risk | `R-n` | `R-1` | In the analysis only |
| Open question | `OQ-n` | `OQ-1` | In the analysis only |
| Goal / Non-goal | `G-n` / `NG-n` | `G-1` | In the intent only |
| Hypothesis | `H-n` | `H-1` | In the intent and validation design |
| ADR | `ADR-NNNN-<kebab-title>.md` | `ADR-0001-python-stack.md` | Superseded or amended, never rewritten |
| Change request | `CR-NNN-<title>.md` | `CR-001-…` | Change mode only |
| Backlog item | `<ABBR>-<phase>-<nn>` | `SL-1-05` | `<ABBR>` = 2–4 letter project abbreviation, the same for all items |
| Policy value | `policy:<key>` = default | `policy:alias.length` = 6 | Configuration, not a literal |

## Statement classes (step 3)
| Class | Signal | Becomes |
|---|---|---|
| **Mandate** | must, shall, never, do not, required, should, may | Requirement, with a Priority (below) |
| **Project activity** | measure, migrate, train, pilot, baseline, report | A roadmap or backlog item, or validation design. **Not** an FR, because it isn't product behaviour |
| **Tunable number** | weights, thresholds, sizes, budgets, SLAs stated as proposals | `policy:<key>` = default (configuration, not a literal) |
| **Illustration** | code samples, example payloads, charts, sample schemas | Design input only |
| **Rationale or research** | citations, "because", comparisons | ADR context or principle |
| **Assumption** | "assume", "we expect", unstated constraints | Constraint table or open question |

**Mandate** (for counting): one source sentence or bullet carrying an obligation, however many clauses it has.

## Priority
| Value | Meaning | Source wording |
|---|---|---|
| `M` | Must | must, shall, never, required |
| `S` | Should | should, unless the source calls it essential (then `M`) |
| `C` | Could | may, could, nice to have |
| `W` | Won't (this time) | explicitly deferred |

## Phase
`P0`–`Pn`. Default order: **measure → foundation → core → intelligence → automation**, unless the source dictates otherwise. **Gated phases** (where every Must needs an AC) default to `P0`, `P1`; change with `--ac-phases`.

## Requirement status
| Value | Meaning |
|---|---|
| `Draft` | Written, not yet agreed. Later-phase Musts may stay Draft without ACs |
| `Agreed` | Approved; a Must needs an AC to reach this |
| `Implemented` | Code exists |
| `Verified` | An AC-named test passes |
| `Withdrawn: <reason or replacement ID>` | Retired; row kept, excluded from gates and budget |

**Live requirement:** any requirement whose status is not `Withdrawn`.

## EARS patterns
| Pattern | Template |
|---|---|
| Ubiquitous | The `<component>` shall `<response>`. |
| Event-driven | **When** `<trigger>`, the `<component>` shall `<response>`. |
| State-driven | **While** `<state>`, the `<component>` shall `<response>`. |
| Unwanted | **If** `<condition>`, **then** the `<component>` shall `<response>`. |
| Optional | **Where** `<feature>`, the `<component>` shall `<response>`. |

**Named component:** the subject is a named part of the product (for example, Link Service, Redirector), never "the system".
**Implementation noun:** a product, library, framework, class or table name. Not allowed in specs. Standards and protocols the owner has confirmed (HTTP, OIDC, TLS, CSV) are allowed.

## Requirement budget
`N = 2 × source mandates + D-n`, **capped at 20 for a one-page brief** (about 40 for a 10-page document). Set once at the end of step 3, recorded in the README status row `Requirement budget` as `<live> / <N>`, enforced by `generate_register.py --budget N`.

## Gates
| Gate | After step | Shows |
|---|---|---|
| **A** Analysis | 3 | Capability map (prefixes, no requirement IDs yet), D-n, top risks, OQs with defaults |
| **B** Specs | 5 | Count per spec and priority against the budget, P0–P1 Musts, late findings, uncertain wording |
| **C** Design and plan | 7 | ADR list, dependency rules, roadmap table |

| Gate value | Meaning |
|---|---|
| `☐ pending` | Not reached |
| `⏳ awaiting approval` | Stopped here for the user |
| `✓ DD-MM-YYYY` | Approved by the user |
| `skipped (run straight through)` | The user asked to run straight through |
| `skipped (user unreachable)` | Autonomous or headless run, and the user did not ask to run straight through |

"Run straight through" skips the gates but **not** the step 2 questions.

## Decision status (README decisions table, intent constraints table)
| Value | Meaning |
|---|---|
| **Confirmed by owner** | The user stated or chose it, including answers already in the request |
| **Default accepted** | The user approved a proposed default unchanged, or could not be asked |
| **Assumed from source** | Never discussed; a candidate for later confirmation |
| **Recorded from code** | Settled by existing code and not asked (Existing codebase mode); has a retrospective ADR |

## Open-question status
| Value | When |
|---|---|
| `Open` | Not decided |
| `Resolved: <decision> (Gate A, DD-MM-YYYY)` | Decided at Gate A approval |
| `Resolved: default accepted (Gate A skipped, DD-MM-YYYY)` | Gate A skipped and the default was applied |
| `Resolved: <decision> (CR-NNN, DD-MM-YYYY)` | Decided by a change request |

## ADR status
`Proposed` · `Accepted (confirmed by owner, DD-MM-YYYY)` · `Accepted (recorded retrospectively, DD-MM-YYYY)` · `Superseded by ADR-XXXX`. Optional line `Amends: ADR-XXXX` for a non-contradicting extension.

## Late-finding tags
Items found after a gate are appended with `(added at step n)` or `(added by CR-NNN)`. Approved rows are never deleted.

## Target agents
| Value | Grader key (`--agents`) |
|---|---|
| GitHub Copilot | `copilot` |
| Claude Code | `claude` |
| Cursor | `cursor` |
| Tool-neutral `AGENTS.md` | `agents-md` |
