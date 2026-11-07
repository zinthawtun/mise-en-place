# ADR-0003: Authenticate on create only
- **Status:** Accepted
- **Date:** 03-11-2026
- **Specs:** FR-SEC-001, FR-RED-001, NFR-RED-001
## Context
The brief says only staff create links, but anyone on the network may open them. An SSO round-trip on redirect would break the latency budget.
## Decision
Require an OIDC token on `POST /api/links` only. Redirects are anonymous.
## Consequences
+ Fast, simple redirects. − Aliases are guessable; accepted under NG-1 (internal only) and R-1.
