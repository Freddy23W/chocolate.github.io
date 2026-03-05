---
description: Plan a task using orga/task structure
auto_execution_mode: 0
---

Goal: Create or update a concrete TODO plan for a specific task.

## 1) Identify task
- Infer the task ID from context (open files, recent edits, `orga/tasks/TASKS.md`); only ask the user if it remains ambiguous.
- `read_file`: the corresponding task folder's `README.md` and `plan.md` (if any).
- `read_file`: `brief.md` in the task folder (planner handoff; if missing, create it).
- If `brief.md` is missing and the canonical planner brief exists, copy it into the task folder:
  - Canonical location: `orga/domain/task-briefs/T-XXX.md`
- Ensure `outcome.md` exists in the task folder (create if missing).
- `read_file`: `orga/tasks/TASKS.md`.

If the task folder does not exist yet and the repo uses the PR-based task lifecycle, dispatch GitHub Actions **Start Task** (no GitHub UI clicks) via:

- `python .github/scripts/dispatch_workflow.py --workflow start-task.yml --ref main --input task_id=T-002 --input title="..." --input auto_merge=true --input delete_branch=false`

If you plan to implement on the Start Task PR branch, fetch and check out that branch locally and push commits to it (the assistant should run these commands when requested; the user should not have to).

2) Plan
- Use `todo_list` to create or update a plan for this task (analysis, design, implementation, tests, smoke tests, docs).
- Treat `brief.md` as the source of truth for the macro intent (context, scope, acceptance notes). The job of `/plan-task` is to translate it into an executable step plan in `plan.md`.
- When planning implementation, prefer modular structure:
  - Keep `app.py` thin (entrypoint/app factory).
  - Put most logic in `src/` packages/modules.
- Ensure the plan explicitly covers how to validate the change:
  - which automated tests to add or update (e.g. pytest), and
  - which smoke tests to run (e.g. core flows or HTTP checks) before marking the task as done.
- Ensure `README.md` includes explicit acceptance criteria and scope boundaries (in/out).
- Keep changes scoped to this task; avoid unrelated refactors.
 - When suggesting implementation steps, prefer grouping work into a small number of meaningful commits that can later be referenced from `outcome.md`'s `## Commit / PR references` section.

3) Record
- Suggest updates to the task's `plan.md` so progress is tracked in the repo, not just in chat.
- Ensure `outcome.md` has the standard headings so results/validation can be recorded during `/work-on-task`, including the `## Commit / PR references` section for mapping tasks -> commits/PRs -> code.
- Encourage updating `outcome.md` during execution (as durable facts emerge), then finalizing it at the end.
- If any brief assumptions change during planning, update `brief.md` (and if used, the canonical `orga/domain/task-briefs/T-XXX.md`) so the handoff stays correct.

Wrap-up (recommended for a no-manual-git flow):

- Run `git status --porcelain`, then commit and push planning/doc changes so they land on GitHub without the user having to run git commands.

Outputs: updated TODO list and clear next steps for this task.
