# Data Model
## 1. Principles
Aliases are immutable once created. Click counts are aggregate integers with no visitor data (NG-2).
## 3. Tables
```sql
CREATE TABLE link (
  alias        text PRIMARY KEY,
  target_url   text NOT NULL CHECK (target_url ~ '^https?://'),
  created_by   text NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now(),
  expires_at   timestamptz NOT NULL,
  click_count  bigint NOT NULL DEFAULT 0   -- ➕ derived from §2 b5
);
```
## 4. Indexes
Primary key on `alias` serves the redirect lookup.
