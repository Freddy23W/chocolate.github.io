# Initializing a project from this template

This template supports **two complementary initialization mechanisms**:

- **Interactive initialization (Windsurf)**: best for capturing project context correctly.
- **Mechanical initialization (GitHub Action)**: best for applying standardized file operations in a PR.

## Template layer vs project layer (important)

- This repository contains both:
  - the **template/workflow layer** (orga/task model, `.windsurf/`, `docs/windsurf/`, GitHub Actions automation), and
  - your **project layer** (application code, project runtime configuration, project-specific docs).
- In a real project created from this template, keep the template/workflow artifacts stable and put your application code under `src/` (plus `app.py`, `tests/`, `templates/` as needed).

Environment note:

- In this template repo, `.env.example` is primarily for **local automation** (GitHub workflow dispatch) and should not be used as your app runtime configuration.
- For project runtime settings, prefer documenting them separately (e.g. in your own `.env.example` sections or separate files) while still keeping `.env` uncommitted.

## Before you begin (recommended)

1) Ensure the workflows exist on the default branch

- GitHub only allows manual `workflow_dispatch` runs for workflow files that exist on the repository’s **default branch**.

2) Configure GitHub Actions permissions

- See `docs/github-actions-setup.md`.
- Minimum requirement for this template’s PR-based workflows:
  - `GITHUB_TOKEN` can write to contents and create PRs.

3) (Optional) Verify with the smoke test

- Run **Smoke Test - GitHub Permissions** (`.github/workflows/smoke-test-github.yml`).
- If it creates a PR successfully, the repo is ready for `Initialize Project`, `Start Task`, and `Finish Task`.

## 1) Interactive initialization (recommended): `/init-project`

Run the Windsurf workflow:

- `/init-project`

Behavior:

- Cascade interviews you for the missing information until it can produce a complete initial project picture.
- It writes a structured summary designed to be highly usable by the AI and humans:
  - `orga/domain/project-brief.md`
- It also seeds lightweight baseline docs:
  - `orga/domain/requirements.md`
  - `orga/domain/architecture.md`
  - `orga/domain/data-model.md`
  - `orga/domain/project-plan.md`
- It records a durable init checklist and evidence in:
  - `orga/domain/init-run.md`
- It initializes the task index and a first task (`T-001`), which acts as the durable per-step checklist for init.

It can also generate or update project-specific Windsurf customizations (rules and skills) so that future Cascade sessions have strong, project-tailored guidance.

The init run is only “complete” once the wrap-up gate is satisfied (git status + commit decision) and recorded in `orga/domain/init-run.md`.

Recommended next step:

- Run `/project-planner` to produce a macro plan and propose candidate tasks.
- For each newly proposed task, have `/project-planner` create/update a canonical handoff brief at:
  - `orga/domain/task-briefs/T-XXX.md`
- Use GitHub Actions **Start Task** to create task folders (PR-based scaffolding).
- **Start Task** copies the canonical brief into the task folder as `brief.md`.
- Then use `/plan-task` (and optionally `/work-on-task`) to execute one task at a time.

## 2) Mechanical initialization: GitHub Action “Initialize Project”

Run the GitHub Actions workflow:

- Actions -> **Initialize Project** -> Run workflow

Optional (no GitHub UI clicks): dispatch it locally via the GitHub API:

- Create a local `.env` (do not commit) based on `.env.example` and set `GH_TOKEN`.
- Then run:
  - `python .github/scripts/dispatch_workflow.py --workflow init-project.yml --ref main --input project_name="My Project" --input init_tasks=true --input purge_legacy_tasks=true --input purge_docs=true --input force=false`

Note: this workflow opens a PR and therefore depends on the GitHub Actions permissions described in `docs/github-actions-setup.md`.

Inputs:

- `project_name` (required)
- `init_tasks` (default: true)
- `purge_legacy_tasks` (default: false)
- `purge_docs` (default: false)
- `force` (default: false)

What it does:

- Opens a PR that can:
  - Sync `docs/windsurf/rules/*` -> `.windsurf/rules/*`
  - Sync `docs/windsurf/workflows/*` -> `.windsurf/workflows/*`
  - Sync `docs/windsurf/skills/*` -> `.windsurf/skills/*`
  - Seed baseline `orga/` domain files
  - Optionally reset `orga/tasks/*` and/or `docs/*` based on the inputs

## 3) Windsurf sync policy (important)

- Runtime configuration lives under `.windsurf/`.
- The reusable copy-pack lives under `docs/windsurf/`.

Whenever `.windsurf/*` changes, the corresponding `docs/windsurf/*` files must be updated and the maintainer must be told to copy/sync.

See:

- `docs/windsurf/SYNC.md`
