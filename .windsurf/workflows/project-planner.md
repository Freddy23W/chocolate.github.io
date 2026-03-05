---
description: Project planner (macro-level).
auto_execution_mode: 1
---



Goal: Maintain a macro-level view of the project (phases, tasks, progress) and keep `orga/domain/project-plan.md` in sync with reality.

## When to run this workflow

- Run this workflow whenever you:
  - Start or complete a phase.
  - Work on a macro-level planning or review task (e.g., phase reviews like T-011 or full-system reviews like T-014).
  - Add or significantly change macro-level tasks in `orga/tasks/TASKS.md` (e.g., new phases, review tasks, operations/compliance work).
- Optionally, during regular project health reviews (e.g., weekly/bi-weekly).

## 1) Gather context

- `read_file`: `orga/tasks/TASKS.md`.
- For each active task of interest, `read_file` its `README.md`, `plan.md`, and `outcome.md`.
  - When reading `outcome.md`, pay attention to the `## Commit / PR references` section as the index from the task to its implementing commits/PRs.
- `read_file`: `orga/domain/project-plan.md`.
- `list_dir`: `orga/domain/task-briefs/` and `read_file` the relevant `T-XXX.md` briefs (canonical handoff per task).
- `read_file`: `orga/domain/requirements.md` (optional, when revisiting scope).
- `read_file`: `orga/domain/data-model.md` and `orga/domain/architecture.md` (optional, when planning technical phases).

## 2) Assess status

- Summarize:
  - Which phases in `project-plan.md` are in progress or completed.
  - Which tasks are active, done, or missing for the current phase.
  - For reviewed tasks, what `outcome.md` (especially `## Commit / PR references`) says about what actually changed (commits/PRs, main touched areas, and validation status).
- Note any architecture hygiene drift that should turn into tasks (e.g., a monolithic `app.py` emerging instead of modular `src/` packages).
- Identify gaps:
  - Important areas with no tasks yet (e.g. tests, CI, docs, operations, smoke tests, and periodic review sessions such as phase reviews or full-system reviews).

## 3) Update or suggest updates

- Propose edits to `orga/domain/project-plan.md` to:
  - Mark completed tasks/phases as done.
  - Add or refine future phases or milestones.
  - For each phase, include a **Tasks** section with a table listing (at minimum):
    - Task ID
    - Title
    - Status (`backlog`/`active`/`done`)
    - Folder link/path
  - Keep those per-phase task tables consistent with `orga/tasks/TASKS.md`.
- When relevant, propose edits to other domain docs in `orga/domain` (e.g., `requirements.md`, `data-model.md`, `architecture.md`) so they stay aligned with the current phases and tasks.
- Propose updates to `orga/tasks/TASKS.md`:
  - New tasks that should be created.
  - Tasks that can be marked done or moved to archive.
- For each newly proposed task `T-XXX`, create or update a canonical brief:
  - `orga/domain/task-briefs/T-XXX.md`
  - Keep it short and macro-oriented: context, intended outcome, scope boundaries, acceptance notes, dependencies, and key file paths.
  - This brief is the handoff artifact consumed by `/plan-task` and copied into each task folder as `brief.md` by GitHub Actions **Start Task**.

## 4) Coordinate with task workflows

- For new or changed tasks, suggest using `/plan-task` on those tasks to create detailed TODO plans.
- Do not create task folders by default. Prefer the GitHub Actions **Start Task** workflow to scaffold task folders via PR unless the user explicitly asks for planner-driven local task creation.
- If the user wants a no-GitHub-UI flow, dispatch the workflow locally via:
  - `python .github/scripts/dispatch_workflow.py --workflow start-task.yml --ref main --input task_id=T-002 --input title="..."`
- Keep the planner itself focused on macro-level coordination; do not duplicate per-task details already tracked in task `plan.md` files.
- Ensure the next tasks list explicitly includes which `orga/domain/task-briefs/T-XXX.md` files were created/updated so the handoff is unambiguous.

Outputs:
- Updated or suggested updates for `project-plan.md`.
- Suggestions for new tasks or status changes in `TASKS.md`.
- When applicable, suggested updates for other domain docs in `orga/domain` (e.g., requirements, data model, architecture).
- A short summary in chat of current phase, key risks, and recommended next tasks.

Wrap-up (recommended for a no-manual-git flow):

- Run `git status --porcelain`, then commit and push the planner changes so they are reflected on the default branch (or in a PR) without the user having to run git commands.
