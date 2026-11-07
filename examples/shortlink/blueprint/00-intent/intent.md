---
id: INTENT-001
title: Shortlink — Product Intent
status: Agreed
version: 1.0.0
source: ../brief.md
---

# Shortlink: Product Intent

## 1. Vision
Every internal URL fits in a sentence. *Short, safe, permanent-enough links for staff.*

## 2. Problem statement
- **Long URLs break.** They wrap and get mistyped, which causes about 40 helpdesk tickets a month.

## 3. Core hypothesis
> **H-1:** Within 3 months of launch, broken-link tickets fall by ≥ 30% against the P0 baseline.

## 4. Goals
| ID | Goal | Measured by |
|---|---|---|
| G-1 | Staff create short links in seconds | Median create time < 10 s (UAT) |
| G-2 | Fewer broken-link tickets | H-1 |

## 5. Non-goals
| ID | Non-goal | Rationale |
|---|---|---|
| NG-1 | Public, internet-facing shortener | Abuse surface; internal need only |
| NG-2 | Per-user click analytics | Brief forbids storing who clicked |

## 6. Actors
| Actor | Description |
|---|---|
| Staff creator | Signed-in employee who creates links |
| Visitor | Anyone on the network opening a link |

## 7. Guiding principles
1. **Measure first.** Record the baseline before building.
2. **Safe by default.** Reject anything that is not http(s).
3. **Privacy by design.** Store counts, never identities.

## 8. Confirmed constraints and assumptions
| Constraint | Decision | Status |
|---|---|---|
| Stack | Python 3.13 + PostgreSQL 17 | Confirmed by owner |
| Hosting | Internal Kubernetes | Assumed from source |
| Identity | Company SSO (OIDC) | Assumed from source |

## 9. Primary success measure
`(baseline_tickets_per_month − tickets_per_month_after_3_months) / baseline_tickets_per_month ≥ policy:success.ticket_reduction (0.30)`
