# HTTP Contracts
| Operation | Specs | Input | Output | Mutating | Guardrails |
|---|---|---|---|---|---|
| `POST /api/links` | FR-LNK-001..003, FR-SEC-001..002 | `{url, alias?}` + SSO token | `201 {alias, short_url}` · `409` · `400` · `401` | Yes | SSO required; http(s) only |
| `GET /{alias}` | FR-RED-001..003 | path alias | `302` · `404` | Counter only | No auth; no visitor data stored |

## Forbidden operations
Updating a link's target. Listing all links anonymously.
