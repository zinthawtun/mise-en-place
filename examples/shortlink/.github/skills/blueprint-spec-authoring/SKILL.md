---
name: blueprint-spec-authoring
description: Create or update a Shortlink spec in blueprint/02-specs using EARS requirements with stable IDs, priorities, phases, sources and Given/When/Then acceptance criteria. Use when adding, changing, withdrawing or refining requirements.
---
# Spec authoring
1. Ground in [intent](../../../blueprint/00-intent/intent.md): the change serves a G-n and violates no NG-n or principle; otherwise stop and raise it.
2. Locate the owning spec via the [catalogue](../../../blueprint/02-specs/README.md). Add a new spec only if no capability owns the behaviour.
3. Cite the source section or add a derived D-n to the [analysis](../../../blueprint/01-analysis/requirement-analysis.md).
4. Allocate the next unused ID. Never reuse or renumber.
5. Write in EARS: named component (Link Service, Redirector, Click Counter), one behaviour, testable, no implementation nouns.
6. Set Pri / Phase (consistent with the [roadmap](../../../blueprint/04-plan/roadmap.md)) / Source.
7. Add ACs (Given/When/Then, concrete values) for every Must.
8. Extract tunable numbers into Policy values.
9. Record unknowns as OQ-n with a default.
10. Propagate to design, ADRs and backlog, then run the blueprint-traceability-audit skill.
## Checklist
- [ ] One behaviour, measurable, named subject, source cited, phase consistent, security considered
