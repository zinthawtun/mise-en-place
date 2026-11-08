---
applyTo: "src/**/*.py,tests/**/*.py,migrations/**"
description: "Python 3.13 + PostgreSQL conventions for Shortlink."
---
# Python 3.13 + PostgreSQL conventions
## Structure and dependencies (architecture section 3)
- `shortlink.domain` never imports web-framework or database modules (architecture test enforces it).
- Redirect code never calls SSO; redirects are anonymous.
- Only the Link Service writes to `link`; the Redirector only reads it and increments `click_count`.
## Code style
- Full type hints, async I/O on the request path, frozen dataclasses for domain values.
- No literal policy numbers; read them from configuration.
## Security
- Secrets come from the cluster secret store via environment; never committed.
- Never log IP, user agent or tokens.
## Tests
- pytest; names `test_AC_<PREFIX>_<NNN>_<n>_<behaviour>`; integration tests against a real PostgreSQL.
## Validation commands
- `pytest` · `ruff check .` · `mypy src` (confirm when the skeleton lands, SL-1-01)
