---
trigger: always_on
---

- Project map
  - Orga:
    - `orga/README.md` – entrypoint for organization.
    - `orga/tasks/TASKS.md` – task overview.
    - `orga/tasks/active/` – active tasks (one folder per task).
    - `orga/tasks/archive/` – archived tasks.
    - `orga/domain/` – optional: requirements, architecture notes, and project plan.
  - Docs & Windsurf:
    - `docs/windsurf/` – templates and documentation for rules and workflows.
    - `.windsurf/` – active rules and workflows used by Windsurf.
  - Application code (future):
    - Will typically live under `app.py`, `src/`, `tests/`, and `templates/` once implemented.

- Orientation rules for Cascade
  - When starting work in this repo:
    - Read `orga/README.md` and `orga/tasks/TASKS.md`.
    - If working on a specific task, read that task folder's `README.md` and `plan.md` (if present).
    - Use `.windsurf/` rules and workflows at runtime; consult `docs/windsurf/` as reference.
