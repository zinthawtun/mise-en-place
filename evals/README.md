# Evals for mise-en-place

For skill maintainers. Running the skill does not need anything in this folder.

| File | Purpose |
|---|---|
| [evals.json](./evals.json) | Trigger cases (should or shouldn't load) and graded scenarios with expectations |
| [HISTORY.md](./HISTORY.md) | Results and fixes from each eval round |
| [grade.py](./grade.py) | Mechanical grader for a finished workspace: layers, EARS subject, technology leaks, requirement budget, policy values, register, links, customisations, status |

## Running a scenario
1. Create a workspace **outside `/tmp`** (some agent sandboxes block it). Copy in the scenario's files, then `git init && git add -A && git commit -m baseline`, so the source document can be diffed.
2. In a fresh agent session with the skill installed, send the scenario's `prompt`. For autonomous runs, add: "You cannot reach the user; proceed with defaults and list them."
3. Grade:
   ```bash
   python3 evals/grade.py <workspace> --source blueprint/brief.md --budget 20 [--agents copilot,claude,cursor,agents-md] [--scan src tests] [--frozen src tests]
   ```
4. Score the judgement-based expectations in `evals.json` by hand, or with a reviewer agent.
