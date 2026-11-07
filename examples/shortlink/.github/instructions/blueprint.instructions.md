---
applyTo: "blueprint/**/*.md"
description: "Rules for authoring blueprint documents."
---
# Blueprint authoring rules
- The source document `blueprint/brief.md` is read-only.
- Keep layers separate (intent / analysis / specs / design / plan / validation). Specs never name classes or libraries.
- IDs `FR|NFR-<PREFIX>-<NNN>` are never reused or renumbered. Withdrawn items are kept.
- EARS wording with a named component as subject. Each row has Pri, Phase and Source.
- ACs `AC-<PREFIX>-<NNN>.<n>` in Given/When/Then form.
- Numbers become `policy:<key>` = default.
- Unknowns become `OQ-n` with a proposed default. Hard-to-reverse decisions become ADRs.
- Use relative links. Regenerate traceability after any spec change.
