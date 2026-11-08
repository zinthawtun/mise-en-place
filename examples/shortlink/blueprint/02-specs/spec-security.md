---
id: SPEC-SEC
title: Security
status: Agreed
version: 1.0.0
phase: P1
source: ../brief.md section 2
---

# Security

## 4. Functional requirements
| ID | Requirement | Pri | Phase | Source | Status |
|---|---|---|---|---|---|
| FR-SEC-001 | If a create request is not authenticated through company SSO, then the Link Service shall reject it. | M | P1 | section 2 b3 | Agreed |
| FR-SEC-002 | If a submitted target URL's scheme is not `http` or `https`, then the Link Service shall reject it. | M | P1 | section 2 b4 | Agreed |
| FR-SEC-003 | Merged into FR-SEC-002 (was "reject javascript: URLs"). | M | P1 | section 2 b4 | Withdrawn |

## 6. Acceptance criteria
- **AC-SEC-001.1**: *Given* no SSO session, *when* a create request arrives, *then* it is rejected as unauthenticated and no link is stored.
- **AC-SEC-002.1**: *Given* a signed-in creator, *when* they submit `javascript:alert(1)` or `file:///etc/passwd`, *then* the request is rejected and no link is stored.
