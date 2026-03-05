---
trigger: always_on
---

- Task model
  - Each task has an ID like `T-001` and a folder under `orga/tasks/active/`.
  - Completed tasks are moved to `orga/tasks/archive/`.
  - `orga/tasks/TASKS.md` is the index of all tasks.

  - Each task folder should include:
    - `brief.md` (planner-to-task handoff; macro context + scope boundaries)
    - `README.md` (goal + scope + acceptance criteria)
    - `plan.md` (execution plan + validation plan + decisions)
    - `outcome.md` (durable results + exact validation commands + follow-ups + commit/PR references)

  - Canonical planner-to-task briefs live under:
    - `orga/domain/task-briefs/` (e.g. `orga/domain/task-briefs/T-002.md`)

- Naming
  - Folder name: `T-XXX-YYYY-MM-DD-short-slug/` (e.g., `T-001-2025-11-14-workflow-setup/`).

- Cascade behavior
  - For each non-trivial task, expect to define and run automated tests and smoke tests as part of considering the task complete.
  - Always identify the current task ID when working on anything more than a tiny change.
  - Prefer to store plans, progress, and decisions in the task's `plan.md` or `notes.md`, not in chat.
  - Prefer to store durable results and validation commands in `outcome.md`.
  - Prefer modular code structure (thin `app.py`, most logic in `src/` modules) rather than a monolithic single-file app.
  - Use the `## Commit / PR references` section in each task's `outcome.md` as the primary index from tasks -> commits/PRs -> code.
  - For single-maintainer repos, prefer a **branchless / low-PR** workflow where implementation happens directly on the default branch while still using task folders and `/plan-task` + `/work-on-task`.
    - Treat GitHub Actions **Start Task** / **Finish Task** workflows as optional helpers for PR-based automation, not mandatory for every task.
  - Keep `TASKS.md` and the task's `README.md` in sync with the actual status.
  - Use `orga/domain/project-plan.md` and the `/project-planner` workflow for macro-level coordination (phases, milestones, and deciding which tasks to tackle next).
    - Run `/project-planner` when starting or completing a phase, or when working on macro-level review/planning tasks (e.g., T-011, T-014, and their successors).
    - During `/project-planner`, ensure `orga/domain/project-plan.md` and other docs in `orga/domain/` (e.g., `requirements.md`, `data-model.md`, `architecture.md`) stay aligned with `orga/tasks/TASKS.md` and the actual implementation.
  - For UX-facing tasks, include explicit UX review steps and affected screens/flows in the task plan.
  - For permissions/roles-sensitive tasks, include an access matrix (who can see/do what) and validation steps (tests + manual checks).
  - For security-sensitive changes, include a brief threat sketch and the tests/smoke checks that will cover the identified risks.
