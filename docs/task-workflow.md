# Task workflow (GitHub + orga)

This template uses a lightweight task model that is reflected in both:

- `orga/tasks/TASKS.md` (canonical task index)
- `orga/tasks/active/` and `orga/tasks/archive/` (task folders)

## Start a task

Recommended:

1. Run GitHub Actions workflow **Start Task**.
2. This creates a PR on a branch like `task/t-002-short-slug`.
3. Merge the PR to add the task folder + update `TASKS.md`.

Optional (no GitHub UI clicks): dispatch Start Task locally:

- `python .github/scripts/dispatch_workflow.py --workflow start-task.yml --ref main --input task_id=T-002 --input title="Short title"`

Notes:

- The workflow creates:
  - `orga/tasks/active/T-XXX-YYYY-MM-DD-short-slug/brief.md`
  - `orga/tasks/active/T-XXX-YYYY-MM-DD-short-slug/README.md`
  - `orga/tasks/active/T-XXX-YYYY-MM-DD-short-slug/plan.md`
  - `orga/tasks/active/T-XXX-YYYY-MM-DD-short-slug/outcome.md`
- If you used `/project-planner`, its canonical brief lives at:
  - `orga/domain/task-briefs/T-XXX.md`
  and is copied into the task folder as `brief.md` by **Start Task**.
- After merging, run `/plan-task` in Windsurf for that task folder.

- During execution, use `/work-on-task` and record durable results, validation commands, follow-ups, and commit/PR references in `outcome.md` as you go, then do a final coherence pass at the end of the task (see the `## Commit / PR references` section).
- Prefer modular code structure: keep `app.py` thin and put most implementation in `src/` modules.

## Branchless / reduced-PR mode (single maintainer)

For a single maintainer working primarily on the default branch (often `main`), it is acceptable—and often simpler—to use a branchless / low-PR workflow:

1. **Create the task folder once**
   - Either run **Start Task** once and merge the scaffold PR.
   - Or, if you prefer to avoid the workflow entirely, create the task folder manually under `orga/tasks/active/` following the naming conventions.
2. **Work directly on `main`**
   - Implement code and docs changes on the default branch instead of opening a dedicated PR for every small task.
   - Keep commits small and meaningful so they can be referenced from the task’s `outcome.md` (`## Commit / PR references`).
3. **Use Windsurf workflows for structure, not for branching**
   - Use `/plan-task` to maintain `plan.md`.
   - Use `/work-on-task` as the main execution loop, keeping `plan.md` and `outcome.md` up to date.
4. **Treat GitHub Actions workflows as optional helpers**
   - **Initialize Project** can still be used once to set up the repo.
   - **Start Task** / **Finish Task** workflows are optional; keep them for larger/riskier changes or collaborative work where PRs are desirable, rather than for every task.

## Finish a task

Recommended:

1. Merge the task’s implementation PR(s).
2. Run GitHub Actions workflow **Finish Task**.
3. This creates a PR that:
   - moves the task folder from `orga/tasks/active/` to `orga/tasks/archive/`
   - updates `orga/tasks/TASKS.md` to set status to `done` and point at the archived folder
4. Merge the PR.

Optional (no GitHub UI clicks): dispatch Finish Task locally:

- `python .github/scripts/dispatch_workflow.py --workflow finish-task.yml --ref main --input task_id=T-002`

- **Task folder naming**: `T-XXX-YYYY-MM-DD-short-slug/`
- **Branch naming**:
  - Start Task creates: `task/t-xxx-short-slug`
  - Finish Task creates: `chore/finish-t-xxx`

## When to use which workflow

- `/project-planner`:
  - Use for macro-level phases, cross-task planning, or major scope changes.
  - Run when starting/completing a phase or doing a broad project review.
  - Typically **skip** for small, self-contained tasks that don't affect the overall project plan.
- `/plan-task`:
  - Use when a new task is created or when an existing task needs a clearer TODO plan.
  - Focus on turning the task's `brief.md` into an executable plan in `plan.md`.
- `/work-on-task`:
  - Use as the main loop for day-to-day implementation work on a single task.
  - Keep `plan.md` and `outcome.md` (including `## Commit / PR references`) in sync with actual progress.
