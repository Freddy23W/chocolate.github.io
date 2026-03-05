---
trigger: always_on
---

- Workflow execution protocol
  - When the user invokes a workflow (e.g. `/init-project`, `/work-on-task`, `/plan-task`, `/project-planner`), you must:
    - Create and maintain an explicit per-step checklist (use `todo_list`).
    - Create or update a durable repo artifact that records workflow progress:
      - Prefer an existing task folder `plan.md` (or `notes.md`) if the workflow relates to a task.
      - Otherwise, create/update `orga/domain/init-run.md` (for initialization) or another clearly named `orga/domain/*` file.
  - Completion rule
    - You must not declare a workflow “done” unless:
      - Every workflow step is marked `done`, or
      - A step is marked `skipped` with a short written justification.
  - Evidence-based completion report
    - When closing a workflow, include a short completion report mapping:
      - workflow step -> evidence (file paths, commands run, `git status` outcome)
  - Quality gates
    - If a workflow requires a wrap-up gate (e.g. `git status`, commit decision), it is mandatory unless explicitly skipped with justification.
