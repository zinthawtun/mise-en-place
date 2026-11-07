# Eval history for mise-en-place

Results from each eval round, newest first. See [README.md](./README.md) for how to run a scenario.

## Round 4 results (07-11-2026, after the budget fixes)
Fresh general-purpose agent, independent workspace, Shortlink brief, four target agents, run straight through.

| Scenario | Result | Fixed in the skill during the run |
|---|---|---|
| 1 New project | `grade.py --budget 20 --agents copilot,claude,cursor,agents-md`: 17/17 on the first run. 16 live requirements (budget 20), 3 specs, 5 derived, 5 ADRs | Grader silently passed unknown agent keys (now FAIL, plus `agents` alias, and `.agents/skills` is checked); gate value when run-straight-through and unreachable overlap; OQ status when Gate A is skipped; mandate counting rule; absolute rules are not policy values |
| Bundled example | 14/14 when copied to a clean git repo with `--agents copilot` | Example now ships the full Copilot customisation set; link to `references/` made portable |

## Round 3 results (07-11-2026, latest skill version)
Run by the evaluating agent, not a fresh session. Scenario 1 reused the eval 4 customisation skills, adapted. Scenario 2 reused scenario 1's analysis and specs, so it checks gate and resume behaviour, not fresh authoring.

| Scenario | Result | Fixed in the skill during the run |
|---|---|---|
| 1 New project | `grade.py --budget 20`: 14/14. 11 requirements (was 32 in round 1), 3 specs, 5 ADRs, register 0 errors, 0 broken links, step 12 recorded | None needed |
| 2 Gates and resume | Stopped at step 3 with Gate A `⏳ awaiting approval`; resume marked Gate A ✓ with date, OQ-3 Resolved (one-row diff in the analysis, no approved rows rewritten); stopped at step 5 with Gate B pending, 11 requirements against budget 20 (was 44), audit-only register OK | None needed |

## Round 2 results (07-11-2026, after the round 1 fixes)
| Scenario | Result | Fixed in the skill during the run |
|---|---|---|
| 3 Change | All 8 expectations met. CR-001 has the verbatim request; new IDs FR-LNK-005/006, FR-SEC-004 (after withdrawn 003), FR-RED-004; OQ-1 resolved; P1 placement; ADR-0004 amends ADR-0003; register 0 errors, 0 broken links | Gates in headless runs: `skipped (user unreachable)` |
| 4 Existing codebase | `grade.py --agents copilot,claude --frozen src tests`: 17/17. 13 requirements (budget 26); Current state table; 2 Verified with named tests, 3 Implemented with `impl:`; 2 retrospective ADRs; P0 characterisation items; team rules kept verbatim | Claude path scope moved to `.claude/rules/` (was nested `CLAUDE.md`, which would have written into `src/`); implemented requirements take Phase P0; `Recorded from code` status; source outside the blueprint is linked, not copied |
| 1 New project, 2 Gates | Re-run in round 3 | — |

## Round 1 results (07-11-2026)
| Scenario | Result | Fixed in the skill since |
|---|---|---|
| Trigger cases + 6 extra paraphrases | 13/13 routed correctly | Description: added discovery notes, kick off, scope, "Not for …" |
| 1 New project | 11/13 at step 9, when the run was cancelled. 32 requirements from 7 mandates | Requirement budget, priority mapping, project activities are not FRs |
| 2 Gates and resume | Stopped at Gate A, then resumed at step 4 in a new session and stopped at Gate B ✓. 44 requirements at Gate B | Gate status values, OQ Status column, late findings, audit-only register before step 9 |
| 3 Change | Friction review only (the run was cancelled) | `references/modes.md` Change mode: CR file, impact table, ID and phase rules, ADR amend |
| 4 Existing codebase | Friction review only (the run was cancelled) | `references/modes.md` Existing-codebase mode, the merge procedure, multiple target agents |
