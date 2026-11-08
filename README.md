<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/logo-dark.png">
    <img src="./assets/logo-light.png" alt="mise-en-place logo" width="240">
  </picture>
</p>

# mise-en-place

**Mise-en-place** is a spec-driven planning skill for turning a business
requirement, PRD, brief, research report, or discovery notes into a traceable
project blueprint before implementation begins.

The blueprint captures intent, requirements, architecture and decisions,
roadmap, validation, and traceability. It can also generate instructions and
skills for the coding agents that will implement the project.

## Install

### GitHub Copilot CLI
```bash
copilot plugin install zinthawtun/mise-en-place
```

Update or remove the plugin with `copilot plugin update mise-en-place` or
`copilot plugin uninstall mise-en-place`.

### Claude Code
```text
/plugin marketplace add zinthawtun/mise-en-place
/plugin install mise-en-place@mise-en-place
```

### Cursor
Clone the repository into Cursor's local plugins folder, then restart Cursor and
check **Customize**:
```bash
git clone https://github.com/zinthawtun/mise-en-place ~/.cursor/plugins/local/mise-en-place
```

### Manual (any agent that supports skills)
Copy [`skills/mise-en-place/`](./skills/mise-en-place/) into your project's
skills folder, for example `.github/skills/`, `.claude/skills/`,
`.cursor/skills/` or `.agents/skills/`.

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
[`references/customisations.md`](./skills/mise-en-place/references/customisations.md) for target
paths and merge rules.

## Repository contents

- [`skills/mise-en-place/`](./skills/mise-en-place/) — the skill:
  - [`SKILL.md`](./skills/mise-en-place/SKILL.md) — instructions and workflow.
  - [`references/`](./skills/mise-en-place/references/) — vocabulary,
    procedures, templates, modes, and agent customisation guidance.
  - [`scripts/`](./skills/mise-en-place/scripts/) — Python 3
    standard-library tools for generating the traceability register and
    checking links.
- [`plugin.json`](./plugin.json), [`.claude-plugin/`](./.claude-plugin/),
  [`.cursor-plugin/`](./.cursor-plugin/) — plugin manifests for Copilot CLI,
  Claude Code, and Cursor.
- [`examples/shortlink/`](./examples/shortlink/) — a complete worked example
  with a brief, blueprint, tests, and Copilot customisations.
- [`evals/`](./evals/) — trigger cases and scenarios for evaluating the skill.

## Maintainer checks

No third-party Python packages are needed. From the repository root, run:

```bash
python3 skills/mise-en-place/scripts/test_scripts.py
python3 evals/grade.py examples/shortlink --source blueprint/brief.md \
  --budget 20 --agents copilot
python3 skills/mise-en-place/scripts/check_links.py examples/shortlink/blueprint examples/shortlink/.github
```

See [`evals/README.md`](./evals/README.md) for running and grading additional
scenarios. When releasing, bump `version` in all three manifests,
`.claude-plugin/marketplace.json`, and `.github/plugin/marketplace.json`, and
add an entry to [`CHANGELOG.md`](./CHANGELOG.md).

## Origin

Before agentic development, the first job on a project was setting up the development environment. With modern AI tooling that job has become easy, but AI-assisted development adds a second setup job: preparing the environment for the agents. While working on some personal projects and improving my own agentic SDLC, I wrote a requirements document for an application and broke it down with GitHub Copilot. That document drew on the requirements and design practices listed in the Pantry. The breakdown became the blueprint structure, and this skill captures that process so it can be repeated.

## Pantry

The ingredients this skill builds on. Each entry says what was borrowed; the combination and the tooling around it are original to this repository.

| Source | Borrowed idea | Where it appears |
|---|---|---|
| [EARS, Easy Approach to Requirements Syntax](https://doi.org/10.1109/RE.2009.9) (Alistair Mavin et al., Rolls-Royce, IEEE RE 2009; [overview](https://alistairmavin.com/ears/)) | Requirement sentence templates | `02-specs/` |
| [Architecture Decision Records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) (Michael Nygard, "Documenting Architecture Decisions", 2011) | One short record per hard-to-reverse decision | `03-design/adr/` |
| [anthropics/skills, skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Eval loop for skills: `evals/evals.json` with should-trigger cases and graded expectations, scripted checks where possible, then revise | [`evals/`](./evals/README.md) |

These are influences on ideas and workflow. The skill also reflects practices picked up from many open-source repositories on GitHub, with no single one as a source; thanks to everyone who shares their work. If I have missed a source that should be credited, please [open an issue](https://github.com/zinthawtun/mise-en-place/issues) and I will add it.

## License

[MIT](./LICENSE)
