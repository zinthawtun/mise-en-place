# ADR-0002: PostgreSQL for links
- **Status:** Accepted
- **Date:** 03-11-2026
- **Specs:** SPEC-LNK, SPEC-RED
## Context
Alias uniqueness (FR-LNK-003) needs a transactional unique constraint. The cluster already runs managed PostgreSQL.
## Decision
Store links in PostgreSQL 17 with `alias` as the primary key.
## Consequences
+ Conflicts are atomic. − A redirect needs a database read; add a cache only if NFR-RED-001 fails.
