# mise-en-place

**Mise-en-place** is a spec-driven planning skill for turning a business
requirement, PRD, brief, research report, or discovery notes into a traceable
project blueprint before implementation begins.

The blueprint captures intent, requirements, architecture and decisions,
roadmap, validation, and traceability. It can also generate instructions and
skills for the coding agents that will implement the project.

## When to use it

Use the skill to:

- Kick off or scope a greenfield project, epic, or major initiative.
- Adopt spec-driven development on an existing codebase.
- Break a requirements document into specifications, design, and a plan.
- Add, change, or resume scope in an existing blueprint.

It is for planning, not implementation. Use the generated
`spec-driven-implementation` skill for backlog items. It is also not intended
for one-off ADRs, bug fixes, or ordinary documentation.

## How to use it

Provide the skill with the path to the source requirements document. You can
also specify a technology stack and blueprint folder:

```text
<path to requirement document> [stack] [blueprint folder]
```

### Example prompts

| Mode | Prompt |
|---|---|
| New | `Use mise-en-place on blueprint/brief.md. Stack: Python 3.13 + PostgreSQL.` |
| New, with approval gates | `Use mise-en-place on blueprint/brief.md with approval stops.` |
| New, without stops | `Use mise-en-place on blueprint/brief.md. Run straight through without approval stops.` |
| From a PRD | `Here's our PRD for the new billing service. Break it down into specs, architecture and a phased plan before we write code.` |
| Existing codebase | `This repo already has code but no specs. Use mise-en-place with docs/vision.md as the source.` |
| Change | `Using mise-en-place, add this to Shortlink: creators can delete their own links. Update everything affected.` |
| Resume | `Continue the mise-en-place blueprint in blueprint/ from where it stopped.` |

The skill should **not** be used for prompts such as
`Implement backlog item SL-1-02` or `Fix the null reference exception in OrderService.cs`.

The skill first inventories the source and existing project, then selects the
appropriate mode:

- **New** — create a complete blueprint for a new project.
- **Existing codebase** — create the blueprint while accounting for the
  current implementation.
- **Change** — record and assess a change to an existing blueprint.
- **Resume** — continue an incomplete blueprint from its first unfinished
  step.

Work proceeds through intake, clarification, requirement analysis, approval
gates, specifications, design, planning, validation, traceability, agent
customisations, and verification. The source document is not edited. Unknowns
and decisions remain explicit, and the skill does not write implementation
code unless asked.

## Blueprint output

A typical output folder contains:

```text
<blueprint>/
├── README.md                 # Status, decisions, and gate outcomes
├── <source>                  # Original requirements (never edited)
├── traceability.md
├── 00-intent/
├── 01-analysis/
├── 02-specs/
├── 03-design/
│   └── adr/
├── 04-plan/
├── 05-validation/
└── changes/                  # Change mode only
```

The skill can also create always-on and path-scoped instructions, project
skills, and a reviewer agent for supported coding-agent environments. See
[`references/customisations.md`](./references/customisations.md) for target
paths and merge rules.

## Repository contents

- [`SKILL.md`](./SKILL.md) — skill instructions and workflow.
- [`references/`](./references/) — vocabulary, procedures, templates, modes,
  and agent customisation guidance.
- [`scripts/`](./scripts/) — Python 3.9+ standard-library tools for generating
  the traceability register and checking links.
- [`examples/shortlink/`](./examples/shortlink/) — a complete worked example
  with a brief, blueprint, tests, and Copilot customisations.
- [`evals/`](./evals/) — trigger cases and scenarios for evaluating the skill.

## Maintainer checks

No third-party Python packages are needed. From the repository root, run:

```bash
python3 scripts/test_scripts.py
python3 evals/grade.py examples/shortlink --source blueprint/brief.md \
  --budget 20 --agents copilot
python3 scripts/check_links.py examples/shortlink/blueprint examples/shortlink/.github
```

See [`evals/README.md`](./evals/README.md) for running and grading additional
scenarios.
