---
name: blueprint-traceability-audit
description: Regenerate and audit the Shortlink requirement register in blueprint/traceability.md; find duplicate IDs, Musts without ACs, backlog phase mismatches, broken links, and code citing unknown or withdrawn IDs. Use after any spec change or before closing a phase.
---
# Traceability audit
1. `python3 .github/skills/blueprint-traceability-audit/generate_register.py --blueprint blueprint --budget 20 --ac-phases P0,P1 --scan src tests`
   Fails on duplicate IDs, gated Musts without ACs, backlog phase mismatches or unknown IDs, and code citing unknown or withdrawn IDs. Warns on gated Musts missing from the backlog or lacking AC-named tests.
2. `python3 .github/skills/blueprint-traceability-audit/check_links.py blueprint .github .claude .cursor .agents CLAUDE.md AGENTS.md README.md`
3. Fix the errors. Explain each warning that remains.
4. Report findings as a table: Severity | ID | File | Finding | Fix. Do not change spec meaning during an audit.
