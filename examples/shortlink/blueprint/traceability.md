# Traceability Matrix
Regenerate §3 with the traceability-audit skill. Do not hand-edit it.

## 1. Source → intent
| Source theme | Intent element |
|---|---|
| §1 Problem | Problem statement, G-2 |
| §3 Success | H-1, primary success measure |
| §2 Privacy | NG-2, principle 3 |

## 2. Spec → design → plan
| Spec | Design artifacts | ADRs | Phases | Backlog |
|---|---|---|---|---|
| [SPEC-LNK](./02-specs/spec-links.md) | [contracts](./03-design/http-contracts.md), [data model](./03-design/data-model.md) | ADR-0002 | P1–P2 | SL-1-01, SL-2-01 |
| [SPEC-RED](./02-specs/spec-redirect.md) | [architecture §4](./03-design/architecture.md) | ADR-0002, ADR-0003 | P1–P2 | SL-1-02, SL-2-01 |
| [SPEC-SEC](./02-specs/spec-security.md) | [contracts](./03-design/http-contracts.md) | ADR-0003 | P1 | SL-1-03 |

## 3. Requirement register

AC ✓ means at least one Given/When/Then acceptance criterion exists. **Must** requirements without ✓ need one before they can move from `Draft` to `Agreed`.

| ID | Pri | Phase | Status | Spec | AC |
|---|---|---|---|---|---|
| FR-LNK-001 | M | P1 | Agreed | [spec-links.md](./02-specs/spec-links.md) | ✓ |
| FR-LNK-002 | S | P1 | Agreed | [spec-links.md](./02-specs/spec-links.md) | ✓ |
| FR-LNK-003 | M | P1 | Agreed | [spec-links.md](./02-specs/spec-links.md) | ✓ |
| FR-LNK-004 | S | P2 | Draft | [spec-links.md](./02-specs/spec-links.md) | ✓ |
| FR-RED-001 | M | P1 | Agreed | [spec-redirect.md](./02-specs/spec-redirect.md) | ✓ |
| FR-RED-002 | M | P1 | Agreed | [spec-redirect.md](./02-specs/spec-redirect.md) | ✓ |
| FR-RED-003 | M | P2 | Draft | [spec-redirect.md](./02-specs/spec-redirect.md) | ✓ |
| NFR-RED-001 | M | P1 | Agreed | [spec-redirect.md](./02-specs/spec-redirect.md) | ✓ |
| FR-SEC-001 | M | P1 | Agreed | [spec-security.md](./02-specs/spec-security.md) | ✓ |
| FR-SEC-002 | M | P1 | Agreed | [spec-security.md](./02-specs/spec-security.md) | ✓ |
| FR-SEC-003 | M | P1 | Withdrawn | [spec-security.md](./02-specs/spec-security.md) |  |
