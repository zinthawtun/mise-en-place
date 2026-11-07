---
name: spec-driven-implementation
description: Implement a Shortlink backlog item from the blueprint specs in a traceable, test-first way. Use when writing or changing source code.
---
# Spec-driven implementation
1. Identify the [backlog](../../../blueprint/04-plan/backlog.md) item and the requirement IDs it satisfies. If none exist, stop and author a spec first.
2. Confirm the item is in the current (or a completed) phase.
3. Load the requirements, ACs, design sections and ADRs.
4. Write failing tests named after the ACs (`test_AC_RED_001_1_...`).
5. Implement the minimum within the architecture dependency rules and principles.
6. Validate: `pytest`, `ruff check .`, `mypy src`.
7. If the design changed, update the spec or design, or add an ADR, in the same change.
8. Update requirement status, run the traceability audit, and use a commit message with IDs.
## Do not
- Add auth to the redirect path, or store/log the IP, user agent or identity of clickers.
- Accept or redirect to non-http(s) schemes.
- Hard-code alias length, expiry, latency budget or other policy values.
- Add per-user click analytics (NG-2).
