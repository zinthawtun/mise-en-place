# Mise en place: Change and Existing-codebase modes

Read this file when step 1 selects **Change** or **Existing codebase** mode. Everything not mentioned here follows the main procedure in [SKILL.md](../SKILL.md).

---

## Change mode

A blueprint exists, its README shows `Mise-en-place step | 12`, and the user adds, changes or removes scope.

### C1. Record the request (replaces "read the recipe")
1. Create `<blueprint>/changes/CR-NNN-<kebab-title>.md` from the change-request template in [templates.md](./templates.md). Use the next free number. Quote the user's request **verbatim**, with the date and the requester.
2. Once written, a CR is immutable, like the source document. Later clarifications go into a new CR or the impact section of the same CR, never into the quoted request.
3. Requirements created by the change cite `CR-NNN` in their `Source` cell.
4. Add a row to the README **Change log** (`CR | Date | Step | Gate | Summary`). Leave `Mise-en-place step` at 12. The change log row tracks progress through this change.

### C2. Impact analysis (replaces steps 2–3)
Read only the intent, the spec catalogue, the specs that own the affected behaviour, the ADR index, the roadmap and the backlog. Then fill the CR's **Impact** table:

| Layer | Question | Typical outcome |
|---|---|---|
| Intent | Does it serve a goal? Does it contradict a non-goal or principle? | If it contradicts one, **stop**. Ask the owner whether to change the intent or drop the request |
| Analysis | Which open questions does it answer? What new derived requirements, risks or open questions does it raise? | Mark answered OQs `Resolved (CR-NNN, date)`. Append new D-n, R-n and OQ-n with "(added by CR-NNN)" |
| Specs | Which capability owns the behaviour? | Prefer an existing capability. Create a new spec only if none fits |
| Design | Contracts, data model, dependency rules, flows? | List the sections to change |
| ADRs | A new decision, or a contradiction of an existing one? | See C4 |
| Plan | Which phase? | See C3 |
| Customisations | Do the stage, principles, stack or conventions change? | Usually no |

Ask questions in one round, and only for decisions the change cannot be made without. Give a proposed default for each. Existing open questions that the request answers do not need asking again.

### C3. Apply (runs steps 4–8 only for the layers marked in the Impact table)
- **IDs:** take the next free number **per prefix**, after the highest existing one, including withdrawn IDs. ACs number per requirement (`AC-LNK-005.1`, `.2`).
- **Changing behaviour:** if the meaning of a requirement changes, withdraw it and add a new ID. A change that only clarifies wording without altering behaviour may edit in place. Note this in the CR.
- **Removing scope:** set the Status to `Withdrawn` and add the reason or the replacement ID. Remove it from backlog items and contracts.
- **Phase:** the change goes in the **earliest phase that has not started**, unless the owner says otherwise. Never add to a closed phase. If the change must go into the current phase, flag this at the gate as scope creep against that phase's exit criterion.
- **Backlog:** add items under that phase using the existing ID pattern. Do not renumber existing items.

### C4. ADRs in Change mode
| Situation | Action |
|---|---|
| A new decision that is hard to reverse | New ADR |
| Contradicts an accepted ADR | New ADR that supersedes it. Change only the old ADR's Status line, to `Superseded by ADR-XXXX` |
| Extends an accepted ADR without contradicting it | New ADR with `Amends: ADR-XXXX` in its header. The old ADR stays unchanged |
| No structural impact | No ADR. Say why in the CR's impact table |

### C5. Gate and finish
- One **change gate** after C3, unless the user said "run straight through". Show the impact table, the new and withdrawn IDs, the phase placement, and any ADRs.
- Then run steps 9, 11 and 12. Run step 10 only if the impact table says the customisations change.
- The report lists only what this change touched.

---

## Existing-codebase mode

Code exists, but there is no blueprint. The blueprint must describe **intended** behaviour and record what already exists **as evidence**. It must not reverse-engineer the code into requirements.

### B1. Intake additions (step 1)
1. Inventory the code: entry points, modules, persistence, external integrations, tests, build and test commands, and existing customisation files.
2. Write a short **Current state** section in `requirement-analysis.md` (section 0): a table of `Area | What exists | Evidence (path) | Gaps against the source`.
3. Behaviour that exists in code but is **not** in the source becomes a derived requirement (`D-n`, "derived from existing code: path") **only if the owner should keep it**. Otherwise it becomes an open question: "Keep, change or remove <behaviour>?"

### B2. Clarification (step 2)
Skip questions the code already settles, such as the stack. Record those answers as ADRs with the status `Accepted (recorded retrospectively, DD-MM-YYYY)`, with the code as their evidence.

### B3. Specs (step 5)
- Write requirements for the **intended** behaviour from the source and the approved D-n, in the same way as for a new project.
- Set Status from evidence:
  - `Implemented`: code exists that appears to satisfy the requirement. Put the path in the `Source` cell after the source reference, for example `section 2 b1; impl: src/notes/store.py`.
  - `Verified`: a test also proves at least one of its ACs. Name the test in the AC line.
  - `Draft` or `Agreed`: not built yet.
- Partial implementations stay `Agreed`. Record the gap in the Current state table.
- **Phase:** `Implemented` and `Verified` requirements take **Phase P0**, because their characterisation tests are P0 work (the register rejects a backlog item scheduled before its requirement). Every P0 Must therefore needs an AC. Gaps take the phase where they will be built.

### B4. Plan (step 7)
- **P0 = Baseline.** It contains:
  - any measurement the source asks for;
  - characterisation tests for every `Implemented` Must that is not yet `Verified`. Each is a backlog item that satisfies those requirement IDs. Its "done when" is the AC test passing, or the AC-named test existing.
  - a backlog item for tagging existing tests with AC IDs.
- Do **not** rename or edit existing tests or code at layout stage ("no code at this stage").
- Later phases follow the usual order for the remaining behaviour.

### B5. Traceability (step 9)
Run the register **without** `--scan` at layout stage, or expect "no AC-named test" warnings for implemented Musts until P0 is done. Mention this in the report. Unknown or withdrawn IDs in code are still errors.

### B6. Customisations (step 10)
Follow the merge procedure in [customisations.md](./customisations.md). Keep every existing team rule verbatim, and add the blueprint sections after them.
