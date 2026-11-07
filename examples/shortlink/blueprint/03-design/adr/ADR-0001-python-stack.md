# ADR-0001: Python 3.13 stack
- **Status:** Accepted (confirmed by owner, 02-11-2026)
- **Date:** 02-11-2026
- **Specs:** all
## Context
The brief says the team knows Python. A 50 ms p95 (NFR-RED-001) is easily met by an async Python web service at 200 rps.
## Decision
Build Shortlink in Python 3.13 as a single async web service.
## Consequences
+ Fits the team's existing skills. − A single process holds both create and redirect. Split later if load demands it.
