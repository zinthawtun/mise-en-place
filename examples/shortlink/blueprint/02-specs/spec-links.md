---
id: SPEC-LNK
title: Link management
status: Agreed
version: 1.0.0
phase: P1
source: ../brief.md §2
---

# Link management

## 1. Purpose
Let staff turn long URLs into short links.

## 2. Scope
**In:** create, custom alias, expiry. **Out:** redirect behaviour ([spec-redirect](./spec-redirect.md)) and authentication ([spec-security](./spec-security.md)).

## 4. Functional requirements
| ID | Requirement | Pri | Phase | Source | Status |
|---|---|---|---|---|---|
| FR-LNK-001 | When a staff creator submits a URL without an alias, the Link Service shall return a short link with a generated alias of `policy:alias.length` characters. | M | P1 | §2 b1 | Agreed |
| FR-LNK-002 | Where a custom alias is requested and is free, the Link Service shall use it. | S | P1 | §2 b1 | Agreed |
| FR-LNK-003 | If a requested custom alias is already in use, then the Link Service shall reject the request and leave the existing link unchanged. | M | P1 | D-2 | Agreed |
| FR-LNK-004 | When a link is created without an expiry, the Link Service shall set its expiry to `policy:link.default_ttl_days` after creation. | S | P2 | §2 b6 | Draft |

## 6. Acceptance criteria
- **AC-LNK-001.1**: *Given* a signed-in creator, *when* they submit `https://intranet/a/very/long/path`, *then* they receive a link whose alias has 6 characters from `[a-z0-9]`.
- **AC-LNK-002.1**: *Given* alias `q3plan` is free, *when* a creator requests it, *then* the link uses `q3plan`.
- **AC-LNK-003.1**: *Given* `q3plan` points to URL A, *when* another creator requests `q3plan` for URL B, *then* the request is rejected as a conflict and `q3plan` still points to A.

## 7. Policy values
- `policy:alias.length` = 6
- `policy:link.default_ttl_days` = 365
