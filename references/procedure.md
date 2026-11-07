# Mise en place: step rules

Detailed rules for each step in [SKILL.md](../SKILL.md). Terms and allowed values are in [vocabulary.md](./vocabulary.md).

## Step 1: intake
1. Read the **whole** requirement document. Use ranged reads for long files and do not skim. Note its nature: formal spec, business brief, research report, meeting notes or a mixture. If the document is missing, unreadable or not a requirement, **stop** and ask for it. Never plan from memory or from the file name. If the source lives outside the blueprint folder, leave it where it is and link to it with a relative path; do not copy or move it.
2. Inventory the repository: existing code, docs, any blueprint, and agent customisations (`.github/`, `.claude/`, `CLAUDE.md`, `.cursor/`, `AGENTS.md`). Choose the mode and tell the user which mode you chose. Never overwrite existing customisations: merge.
3. Take working notes on the components, actors, flows, numbers, constraints, assumptions, phases and explicit "do / do not" statements.
4. Read [templates.md](./templates.md) (and [modes.md](./modes.md) if the mode needs it). Create `<blueprint>/README.md` from its template, with the status table and only the layers that exist so far.

**Long sources (more than ~30 pages).** Build the breakdown table (step 3) section by section as you read, and write it to disk early. From then on, work from the analysis and re-read only the source sections you cite. Do not hold the whole document in context.

**Resume mode.** Read the README status, its decisions table, and the analysis's open questions. Continue from the first step that isn't complete. Never redo a layer whose gate is `✓`. If the user's message approves a gate that is `⏳`, record the approval first.

## Step 2: clarification
Ask, in **one** round, only the decisions that change the shape of the output **and** that the user's request, the document or (in Existing codebase mode) the code has not already settled. Propose defaults from the document:

- Implementation stack and runtime
- Hosting and deployment model
- Product or solution name (if the document uses a placeholder)
- Blueprint folder name (default `blueprint/`)
- Target agent(s) for customisations (default: the one you are running in)
- Approval stops at gates A/B/C, or run straight through (default: stops)
- Spec style (default: EARS + stable IDs + Given/When/Then)
- Any assumption in the document that materially changes the architecture

Record every answer in the README **Decisions from clarification** table with a decision status. Step 4 copies these decisions into the intent's constraints table. Anything never discussed is **Assumed from source**.

**Asking the user.** Use the structured question tool if one exists (`ask_user`, `AskUserQuestion` or similar). Otherwise ask one numbered list of questions in plain text, with the proposed default after each, and stop until the user answers. If the user can't be reached (an autonomous or headless run), proceed with the defaults, record them as **Default accepted** and list them in the report. Gates also proceed and are listed in the report as needing review.

## Step 3: analysis
Classify every statement in the source using the statement classes. Then write `requirement-analysis.md` and `glossary.md`:

- **Capability map.** Group mandates into capabilities, each with a 3-letter prefix. Always include a cross-cutting **security** capability if the system touches data, credentials, networks or AI. Add an operations capability (`OPS`) only if the source **states** operational behaviour (backup, uptime, observability). A hosting platform alone ("runs on Kubernetes") is not a mandate: put probes and metrics in the design's deployment section, not in specs.
- **Breakdown table.** Map source section → key mandates → spec → phase. Every substantive source section must appear.
- **Derived requirements** (`D-n`). Things the source implies but never states and that the system would be **wrong or unsafe** without (test: would a reviewer call the system broken if it were missing?): error and edge cases, conflicts, isolation, security, and data lifecycle. Cite what each is derived from. Ideas that are merely nice to have become `OQ-n`, not D-n and not requirements. Keep D-n to about 5 for a one-page brief.
- **Risks** (`R-n`) with likelihood, impact and mitigation.
- **Open questions** (`OQ-n`), each with what it blocks, a **proposed default** and a status, so planning never stalls.
- **Glossary.** Define every domain term once.
- **Budget.** Set the requirement budget N and record it in the README.

## Step 4: intent
`00-intent/intent.md`: one-line vision, problem statement, testable hypothesis or value proposition, goals (`G-n`, each with a measure), non-goals (`NG-n`, each with a rationale), actors, numbered principles, the constraints table (from the decisions table), and the primary success measure. Non-goals matter as much as goals, because they stop scope creep later.

## Step 5: specs
For each capability, create `spec-<capability>.md` from the template:

- **IDs** are never reused or renumbered. Retired ones stay with the status `Withdrawn: <reason>`.
- **EARS wording** with a named component as subject. Each requirement covers one behaviour and must be testable. No implementation nouns.
- **Cross-cutting requirements** live in the spec of their **concern**. A scheme check performed by the Redirector belongs in the security spec, with the Redirector as subject. The spec catalogue lists the components each spec constrains.
- **Attributes:** Priority, Phase, Source (section, `D-n` or `CR-NNN`) and Status. NFRs inherit the phase in the spec's front matter.
- **Acceptance criteria:** Given/When/Then with concrete values. **Every Must in P0–P1 needs one.** Later-phase Musts may stay `Draft` without ACs.
- **Policy values** section for every tunable number. Fixed rules the source states as absolute ("never anything other than http or https") stay in the requirement text, not in policy.
- **Consistency.** Every backlog item's "Done when" names existing ACs, so give an AC to every requirement a backlog item satisfies, including Should and Could ones. Where the system generates a value (alias, ID), state what happens on a collision. Every goal measure in `intent.md` is carried by a requirement or `policy:` value. A requirement or AC never depends on something in a later phase: an AC that uses another requirement's behaviour (an expired link, a click count, a signed-in user) ends with `Needs: <IDs>`, and `generate_register.py` fails if a needed requirement is in a later phase. Fix by moving the requirement earlier, or by rewording the AC to use only what exists in its phase. A backlog item lists, in "Done when", every other item whose output its ACs need. Numbers the source does not give (loads, windows, sizes) are `policy:` values marked as assumptions in the analysis, and every AC cites them by policy key rather than a literal. Split any requirement with more than one "shall" or joined by "and" into separate behaviours, each with its own AC. Every mandate in the source traces to a requirement ID in `traceability.md` §1. Every value an OQ default or AC relies on (alphabet, length bounds, timing, load) is stated in a requirement or `policy:` value. ACs and examples must not contradict the analysis. Timing-dependent behaviour (for example asynchronous counters) states its consistency bound in the requirement. Every behaviour a source statement mandates traces to a requirement, not only to intent. Backlog items satisfy requirements, never ADRs alone.
- **Budget.** Live requirements must not exceed N. Merge, or demote to an `OQ-n`, before Gate B.
- **Open questions don't create requirements.** An OQ default may settle the wording of an existing requirement, but never adds a new FR or NFR. Extra scope (renew, delete, edit, dashboards) stays an `OQ-n` until the owner asks for it.
- **Late findings.** A new D-n or OQ-n found while writing specs is appended to the analysis with "(added at step 5)" and flagged at Gate B.

## Step 6: design
- `architecture.md`: C4 context, containers and components (Mermaid). Give **explicit dependency rules** that can be enforced by tests. Show the key sequence flows, the solution or folder layout, and a technology table linked to ADRs.
- `data-model.md` (if data persists): entities, tables with additions to the source marked ➕, indexes, and mutation rules such as append-only.
- Interface contracts for every external surface: inputs, outputs, read-only versus mutating, and forbidden operations.
- **ADRs**, one per hard-to-reverse decision: the system boundary, stack, storage, trust or security posture, integration style, source-of-truth ownership, and "numbers are configuration". Mark owner-confirmed ones as confirmed, with the date. Every ADR lists at least two real alternatives and why each was rejected; a decision with no alternative is a constraint, not an ADR.

## Step 7: plan
- `roadmap.md`: phases in the default phase order unless the source dictates otherwise. Each phase has a deliverable and an **exit criterion**, taken from the source where possible. Add phase gates, and a Gantt chart if the source gives dates.
- `backlog.md`: rows `| <ABBR>-<phase>-<nn> | item | satisfies IDs | done when |`. An item's phase must not be earlier than the phase of any requirement it satisfies. Detail only the first 2 phases. Later phases are epics.

## Step 8: validation design
`05-validation/validation-design.md`: how the project proves it worked. This could be experiments (hypotheses, treatments, protocol, metrics, pre-registered success criteria, threats to validity), benchmarks, UAT or KPIs. If the source states a hypothesis, this file is mandatory.

## Step 9: traceability
1. Write `traceability.md` with §1 source→intent, §2 spec→design→ADR→phase→backlog, and a heading `## 3. Requirement register`.
2. Generate the register with `generate_register.py --budget <N> [--scan src tests]`. It exits 1 on:
   - duplicate IDs
   - more live requirements than `--budget N`
   - a gated-phase Must with no acceptance criterion
   - a backlog item in an earlier phase than a requirement it satisfies, or citing an unknown ID
   - with `--scan`, code that cites unknown or withdrawn IDs

   Use `--check` in CI to fail without writing when the register is out of date. Run `--help` for all options.
3. Fix every error. Review the warnings.

## Step 10: customisations
Using [customisations.md](./customisations.md), create or merge the following for **each** target agent:
- Always-on instructions: blueprint reading order, current stage, non-negotiable principles, stack, traceability conventions. With several targets, use one canonical file plus pointers.
- Path-scoped instructions for blueprint docs, for source code in the chosen stack, and for any other content type the project owns.
- Project skills: `<blueprint>-spec-authoring`, `<blueprint>-adr`, `<blueprint>-traceability-audit` (with **both scripts copied in**) and `spec-driven-implementation`.
- A read-only `spec-reviewer` agent.
- A short root `README.md` that links into the blueprint, if none exists.

## Step 11: verify
1. `check_links.py <blueprint> .github .claude .cursor CLAUDE.md AGENTS.md README.md`. Fix every broken relative link. Paths that don't exist only produce a warning.
2. Re-run `generate_register.py --budget <N>`. It must exit 0.
3. If the skill's `evals/grade.py` is present, run it as a final self-check and fix every FAIL:
   `python3 <skill>/evals/grade.py . --source <blueprint>/<source>.md --budget <N> --agents <grader keys>`
4. **Content review, mandatory.** Review the specs, design and plan against this checklist, using a read-only subagent if available, otherwise yourself line by line. Fix every defect, then re-run steps 1–2:
   - Each requirement is one behaviour (one "shall", no "and" joining two), with a named component and a testable AC.
   - Every AC is concrete; every value it uses is in the requirement or a `policy:` key; it contradicts nothing in the analysis; its `Needs:` lists every other requirement it relies on, none in a later phase.
   - Every parameter the analysis resolves (alphabet, length bounds, case, timing, load) appears in a requirement or `policy:` value and is tested by an AC, including both bounds of a range.
   - Generated values state collision behaviour; asynchronous behaviour states its consistency bound.
   - Every ADR has two or more real alternatives with rejection reasons.
   - Specs name no product or library.
   - Every phase has an exit criterion that is not circular; every backlog item satisfies a requirement with ACs (project activities excepted) and lists the items it depends on.
   - Every input, option or field in an interface contract is covered by a requirement and an AC, including invalid values. Every qualifier in a mandate ("on the network", "when free", "should expire") appears in a requirement, not only in a non-goal or note.
   - A field or rule the design applies from the first build (a NOT NULL column, a response field) is defined by a requirement in that phase or earlier. A phase-1 behaviour never leans on a later-phase definition (for example "active" meaning not expired).
   - A range or limit has an AC just inside and just outside each bound, and a retry limit has an AC for the last allowed attempt.
   - A mandate's "should" keeps its priority on the whole behaviour; only a separately stated rule (such as rejecting a taken alias) may rank higher.
   - Every AC lists in `Needs:` any precondition requirement, such as sign-in. Each requirement's EARS sentence has the named component as the subject of "shall".
   - Backlog items sit under the heading of their own phase, and links in table cells are well formed.
   - Every source mandate traces to a requirement ID; every goal measure is carried by a requirement or `policy:` value.
5. Check the Definition of done.

## Step 12: report
Summarise concisely:
- The mode and the files created or merged, grouped by layer
- Counts: capabilities, requirements (against the budget), ACs, ADRs, phases
- The decisions recorded as Default accepted, and judgement calls worth checking
- Open questions that block the next phases, and any conflicts with existing customisations
- The commands that keep the blueprint healthy

Set `Mise-en-place step` to 12. Do not commit unless asked.
