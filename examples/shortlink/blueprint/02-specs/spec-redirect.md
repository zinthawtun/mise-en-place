---
id: SPEC-RED
title: Redirect
status: Agreed
version: 1.0.0
phase: P1
source: ../brief.md §2
---

# Redirect

## 1. Purpose
Send visitors from an alias to its target URL, quickly.

## 4. Functional requirements
| ID | Requirement | Pri | Phase | Source | Status |
|---|---|---|---|---|---|
| FR-RED-001 | When a visitor requests an active alias, the Redirector shall redirect to the link's target URL. | M | P1 | §2 b2 | Agreed |
| FR-RED-002 | If a visitor requests an unknown or expired alias, then the Redirector shall return a not-found page. | M | P1 | D-1 | Agreed |
| FR-RED-003 | When the Redirector serves a redirect, it shall increment that link's click count without recording the visitor's identity. | M | P2 | §2 b5 | Draft |

## 5. Non-functional requirements
| ID | Requirement | Pri | Status |
|---|---|---|---|
| NFR-RED-001 | The Redirector shall serve redirects within `policy:redirect.p95_ms` at the 95th percentile under `policy:redirect.load_rps`. | M | Agreed |

## 6. Acceptance criteria
- **AC-RED-001.1**: *Given* active alias `q3plan` → `https://intranet/x`, *when* a visitor opens `/q3plan`, *then* the response is a redirect to `https://intranet/x`.
- **AC-RED-002.1**: *Given* alias `old1` expired yesterday, *when* a visitor opens `/old1`, *then* the response is the not-found page.
- **AC-NFR-RED-001.1**: *Given* 10,000 active links and 200 requests per second for 5 minutes, *when* latency is measured, *then* p95 ≤ 50 ms.
- **AC-RED-003.1**: *Given* active alias `q3plan` with 0 clicks, *when* a visitor opens `/q3plan`, *then* its click count becomes 1 and no visitor identity is stored with the click.

## 7. Policy values
- `policy:redirect.p95_ms` = 50
- `policy:redirect.load_rps` = 200
