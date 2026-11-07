# Shortlink: Copilot Instructions

Every internal URL fits in a sentence.

## Source of truth: the blueprint
Before planning or changing anything:
1. Read [blueprint/00-intent/intent.md](../blueprint/00-intent/intent.md).
2. Find the relevant spec in [blueprint/02-specs/](../blueprint/02-specs/README.md) and the requirement IDs the work satisfies.
3. Check [architecture](../blueprint/03-design/architecture.md) and the [ADRs](../blueprint/03-design/adr/README.md).
4. Confirm the work belongs to the current phase in [roadmap](../blueprint/04-plan/roadmap.md).

Never edit `blueprint/brief.md`. If a request conflicts with the blueprint, say so and propose a spec change or ADR.

## Current stage
P0: Measure

## Non-negotiable principles
- Only `http` and `https` targets. Reject everything else.
- Never store visitor identity.
- Policy numbers come from configuration, never literals.

## Traceability
- Commits: `<type>(<component>): <summary> [FR-XXX-NNN]`. Tests: `test_AC_XXX_NNN_n_<behaviour>`.
