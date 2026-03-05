# Template Repository

This repository is a reusable starting point for new projects.

- Template/workflow layer: `orga/`, `.windsurf/`, `docs/windsurf/`, GitHub Actions.
- Project layer: your app code (typically `src/`, `app.py`, `tests/`, `templates/`).

## Getting started

- `docs/initializing-a-project.md` – the recommended first-run sequence (Windsurf `/init-project` + GitHub “Initialize Project”).
- `docs/github-actions-setup.md` – required GitHub settings so Actions can create branches and PRs.

## Initialization (recommended)

1. In your IDE, run the Windsurf workflow:
   - `/init-project`

   This interactively gathers the project requirements and generates:
   - `orga/domain/project-brief.md` (AI-ready summary)
   - `orga/domain/requirements.md`
   - `orga/domain/architecture.md`
   - `orga/domain/data-model.md`
   - `orga/domain/project-plan.md`

2. (Optional) In GitHub, run the Actions workflow:
   - **Initialize Project**

   This creates a PR that can:
   - Sync `docs/windsurf/*` -> `.windsurf/*`
   - Create/seed baseline `orga/` files
   - Optionally reset `docs/*` and/or `orga/tasks/*` depending on inputs

## Documentation

- `docs/README.md` – documentation index for this template.
- `docs/windsurf/` – copy-pack for `.windsurf/` (see `docs/windsurf/SYNC.md`).
- `orga/` – task tracking and domain docs.
