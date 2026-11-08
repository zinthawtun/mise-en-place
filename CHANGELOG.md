# Changelog

## 1.0.1 (2026-11-08)

Fixes to the approval workflow, documentation rendering, and Python support
policy. No change to the blueprint output format.

### Fixed
- A rejected approval gate now stays awaiting approval. The skill revises that
  layer and presents it again, and does not start the next step until it is
  approved. If the user cannot be reached, it proceeds on defaults and flags
  the gate for review.
- The report step and final checklist state explicitly that nothing is
  committed unless the user asks.
- The verify step runs `evals/grade.py` only when it exists, using the command
  documented in the procedure.
- A broken table row in the `SKILL.md` file index is fixed.
- The `--budget` help text in `evals/grade.py` now points to
  `references/vocabulary.md` and gives the correct budget guidance.

### Changed
- Minimum supported Python is now 3.12. The CI matrix tests 3.12 and 3.13.
- The skill description is shorter and easier to scan.
- The per-agent output line names the four supported targets: Copilot, Claude
  Code, Cursor, and AGENTS.md.
- The `§` symbol is replaced with the word "section" throughout the references,
  templates, and Shortlink example. The traceability register generator is
  unaffected.

### Documentation
- The README has an Origin section explaining how the skill came about, and a
  Pantry section crediting EARS, Architecture Decision Records, and Anthropic's
  skill-creator.

## 1.0.0 (2026-11-07)

Initial release of mise-en-place, a spec-driven planning skill that turns
requirements into a traceable project blueprint before implementation begins.

### Highlights
- Supports new projects, existing codebases, scope changes, and resuming an
  incomplete blueprint.
- Produces structured intent, EARS requirements, architecture and ADRs, a
  phased roadmap and backlog, validation guidance, and a traceability register.
- Generates coding-agent customisations to keep implementation aligned with the
  approved blueprint.
- Available as a plugin for GitHub Copilot CLI, Claude Code, and Cursor, or as a
  skill copied into another supported agent environment.
- Includes standard-library scripts for register generation and link checking,
  a complete Shortlink example, and evaluation scenarios.
