---
description: Work on a task (execution loop)
auto_execution_mode: 3
---

Goal: Execute a single task end-to-end while keeping the chat tightly aligned with the task state.

1) Start-of-session
- Identify the current task ID (or create one).
- `read_file` the task folder `README.md` and `plan.md` (or create them if missing).
- `read_file` the task folder `brief.md` (planner handoff; create if missing).
- Ensure `outcome.md` exists in the task folder (create if missing).
- Restate the task’s definition of done.
- If the task folder does not exist yet and the repo uses the PR-based task lifecycle, dispatch GitHub Actions **Start Task** (no GitHub UI clicks) via:
  - `python .github/scripts/dispatch_workflow.py --workflow start-task.yml --ref main --input task_id=T-002 --input title="..." --input auto_merge=true --input delete_branch=false`

When using Start Task for a no-click workflow, treat the created PR branch as the implementation branch:

- Push your commits to the Start Task branch; the PR updates automatically.
- If auto-merge is enabled, merging happens automatically once branch protection requirements pass.

In a no-manual-git flow, the assistant should perform the git operations needed to:

- Fetch the Start Task branch
- Check it out locally
- Commit progress in small batches
- Push updates to GitHub

2) Execution loop (repeat)
- Make small, safe edits in batches.
- Run a minimal smoke check when relevant.
- Keep notes/decisions in the task’s `plan.md` or `notes.md`.
- Maintain a small `todo_list` (3–5 items) for this task using the Windsurf `todo_list` tool and update it as work progresses; mirror the same checklist structure in `plan.md`.
- Record durable results in `outcome.md` during execution (what changed, why, validation, follow-ups), then do a final coherence pass near the end of the task.
- Keep the `## Commit / PR references` section up to date with the commits/PRs created during this work.
- Avoid a monolithic `app.py`: keep `app.py` as a thin entrypoint/app-factory and put most implementation in `src/` modules.
- Treat `brief.md` as stable context. If execution reveals the brief is wrong, update `brief.md` and record the correction (and rationale) in `plan.md`.

3) End-of-message status block (recommended)
- For longer or multi-step work, include a short status block:
  - Done in this step
  - Open / next actions
  - Blockers (if any)
  - Suggested command(s) to run (if needed)

4) Finish
- Ensure the task closure gates are satisfied (or explicitly waived with justification in `outcome.md`):
  - Documentation gate: `README.md`, `brief.md`, `plan.md`, and `outcome.md` are up to date.
  - Validation gate: tests and/or smoke checks are recorded in `outcome.md` with exact commands.
  - Traceability gate: the `## Commit / PR references` section in `outcome.md` lists the commits and/or PRs that implemented this task.
  - Repo cleanliness gate: `git status --porcelain` is clean (or deviations explicitly recorded).
- Update task status in `orga/tasks/TASKS.md`.
- Dispatch GitHub Actions **Finish Task** only after the above:
  - `python .github/scripts/dispatch_workflow.py --workflow finish-task.yml --ref main --input task_id=T-002 --input auto_merge=true`
- If any runtime `.windsurf/` files were changed, sync the corresponding `docs/windsurf/` files (see `docs/windsurf/SYNC.md`).
