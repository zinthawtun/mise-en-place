---
name: blueprint-adr
description: Record a Shortlink architecture decision as an ADR in blueprint/03-design/adr. Use when choosing or changing technology, storage, integration boundaries, security posture, dependency rules, or any costly-to-reverse decision, or when superseding an ADR.
---
# ADR authoring
1. Check the [index](../../../blueprint/03-design/adr/README.md). To change a decision, supersede it. Never rewrite history.
2. Take the next number `ADR-NNNN-<kebab-title>.md`.
3. Write Context (forces, IDs, evidence), Decision (active voice) and Consequences (positive, negative, follow-ups).
4. Mark any superseded ADR (change its Status line only). For a non-contradicting extension, add `Amends: ADR-XXXX`.
5. Update the index, architecture section 6 and traceability section 2.
## Template
```markdown
# ADR-NNNN: <Decision>
- **Status:** Proposed | Accepted (confirmed by owner, DD-MM-YYYY) | Superseded by ADR-XXXX
- **Amends:** ADR-XXXX (optional)
- **Date:** DD-MM-YYYY
- **Specs:** SPEC-<PREFIX>, FR-...
## Context
## Decision
## Consequences
```
