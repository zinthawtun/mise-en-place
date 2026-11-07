# Shortlink: one-page brief (source, never edited)

## 1. Problem
Staff paste very long intranet URLs into chat and documents. They wrap, break and get mistyped, and the helpdesk logs about 40 "broken link" tickets a month.

## 2. What we want
- Staff must be able to turn a long URL into a short link. A custom alias should be possible when it is free.
- Opening a short link must redirect quickly. We are thinking under 50 ms at the 95th percentile.
- Only signed-in staff (company SSO) may create links. Anyone on the network may open them.
- Never redirect to anything other than http or https.
- Count clicks per link, but do not store who clicked.
- Links should expire, perhaps after a year by default.
- Aliases of about 6 characters look right.

## 3. Success
We believe Shortlink will cut broken-link tickets by 30% within three months of launch. Measure the current ticket rate before building anything.

## 4. Assumptions
Hosted on the existing internal Kubernetes cluster. The team knows Python.
