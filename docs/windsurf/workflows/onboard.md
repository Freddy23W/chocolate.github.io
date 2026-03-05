---
description: Onboard to this repository
auto_execution_mode: 1
---

Goal: Quickly understand the organization, tasks, rules, and skills for this repo before making changes.

1) Discover structure
- Use `list_dir` at the repo root and at `orga/`.
- Look for `docs/windsurf/` and any existing app code (`app.py`, `src/`, `templates/`).
- If present, also look for `.windsurf/skills/` and `docs/windsurf/skills/`.

Also check:

- `list_dir`: `orga/tasks/`
- Verify `orga/tasks/active/` exists (create it if missing only if you are explicitly asked to apply fixes).
- If `orga/tasks/TASKS.md` exists, spot-check that folders referenced in the table exist.
- If `orga/_legacy/` exists, note that it is reference/example content and should not be used for new tasks.

2) Read core orga docs
- `read_file`: `orga/README.md`.
- `read_file`: `orga/tasks/TASKS.md`.
- If working on a specific task, `read_file` that task folder's `README.md` and `plan.md` (if present).
- `read_file`: `docs/windsurf/rules/project-map.md`.
- If present, `read_file`: `docs/windsurf/skills/project-onboarding/SKILL.md`.

3) Capture a plan
- Use `todo_list` to create or update a TODO plan for the user's requested task.

4) Summarize context
- Post a short summary: structure, current task (if any), and immediate next actions.
