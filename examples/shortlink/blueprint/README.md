# Shortlink Blueprint

This folder is the **blueprint of Shortlink**: the single source of truth for *why* it exists, *what* it must do and *how* it is designed. Code, tests and customisations are downstream.

## Layout
| Layer | Folder | Answers |
|---|---|---|
| Source | [brief.md](./brief.md) | Original requirement (never edited) |
| 0. Intent | [00-intent/](./00-intent/intent.md) | Why, hypothesis, goals, non-goals |
| 1. Analysis | [01-analysis/](./01-analysis/requirement-analysis.md) | Breakdown, risks, open questions, [glossary](./01-analysis/glossary.md) |
| 2. Specs | [02-specs/](./02-specs/README.md) | What each capability must do |
| 3. Design | [03-design/](./03-design/architecture.md) | Architecture, data, contracts, [ADRs](./03-design/adr/README.md) |
| 4. Plan | [04-plan/](./04-plan/roadmap.md) | Phases and [backlog](./04-plan/backlog.md) |
| 5. Validation | [05-validation/](./05-validation/validation-design.md) | How success is proven |
| Traceability | [traceability.md](./traceability.md) | Source → spec → design → plan |

## Reading order
Intent → Analysis → Spec index → Architecture + ADRs → Roadmap

## Status
| Item | Value |
|---|---|
| Stage | Layout and planning complete |
| Mode | New |
| Mise-en-place step | 12 of 12 |
| Requirement budget | 10 / 20 |
| Gates | Analysis ✓ 02-11-2026 · Specs ✓ 03-11-2026 · Design and plan ✓ 04-11-2026 |
| Current phase | P0 |
| Stack | Python 3.13, PostgreSQL 17 |
| Owner | Platform team |

## Decisions from clarification
| Question | Answer | Status |
|---|---|---|
| Stack | Python 3.13 + PostgreSQL 17 | Confirmed by owner |
| Blueprint folder | `blueprint/` | Default accepted |
| Target agent | GitHub Copilot | Confirmed by owner |
| Approval stops | Gates A, B, C | Default accepted |

## Change log
| CR | Date | Step | Gate | Summary |
|---|---|---|---|---|
