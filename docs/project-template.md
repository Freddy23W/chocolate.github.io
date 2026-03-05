# Project Template Summary (Reusable Blueprint)

This document is a **domain-agnostic blueprint** extracted from this repository. It is intended to be used as a setup reference for **new, unrelated projects** (e.g. student feedback collection, lecture management) while reusing the same:

- Orga/task planning workflow
- Windsurf/Cascade rules and workflows
- Flask app structure
- Data handling conventions (data root, uploads, backups)
- Testing/CI conventions
- Deployment and operations patterns (systemd + nginx reverse proxy; optional path prefix)

---

## 1. First steps (bootstrapping a new repo for /project-planner + /plan-task)

This section describes the minimum structure and files you should create so you can immediately manage development with `/project-planner` and `/plan-task`.

1. Create the baseline folders:
 
    - `orga/`
    - `docs/`
    - `.windsurf/rules/`
    - `.windsurf/workflows/`
 
2. Create the orga entrypoints:
 
    - `orga/README.md`
      - Link to `orga/tasks/TASKS.md` and `orga/domain/project-plan.md`.
    - `orga/tasks/TASKS.md`
      - Create the canonical task index table.
    - `orga/domain/project-plan.md`
      - Create the macro plan document (phases + key tasks).
 
3. Copy/adapt the Windsurf runtime configuration:
 
    - Rules:
      - `.windsurf/rules/ai-behavior.md`
      - `.windsurf/rules/project-map.md`
      - `.windsurf/rules/task-workflow.md`
    - Workflows:
      - `.windsurf/workflows/project-planner.md`
      - `.windsurf/workflows/plan-task.md`
      - `.windsurf/workflows/project-review.md` (optional but recommended)
      - `.windsurf/workflows/onboard.md` (optional but useful)
 
4. Create your first task folder and run `/plan-task`:
 
    - Pick the first task ID (e.g. `T-001`) and create:
      - `orga/tasks/active/T-001-YYYY-MM-DD-short-slug/brief.md`
      - `orga/tasks/active/T-001-YYYY-MM-DD-short-slug/README.md`
      - `orga/tasks/active/T-001-YYYY-MM-DD-short-slug/plan.md`
      - `orga/tasks/active/T-001-YYYY-MM-DD-short-slug/outcome.md`
    - Add the task row to `orga/tasks/TASKS.md`.
    - (Optional but recommended) create the canonical planner brief location:
      - `orga/domain/task-briefs/T-001.md`
    - In the IDE chat, run:
      - `/plan-task`
    - Use the resulting TODO plan as the “definition of done” for the task.
 
5. Establish the planning loop:
 
    - At the start of a phase (or weekly), run:
      - `/project-planner`
    - For each concrete task you start, run:
      - `/plan-task`

---

## 2. Repository structure (recommended baseline)

Top-level layout:

- `app.py`
  - Flask app factory (`create_app()`) and main entry point.
  - Keep it thin: avoid accumulating business logic here; put most implementation in `src/` modules.
- `src/`
  - Domain packages (one per bounded context/feature area).
  - Infrastructure modules:
    - `src/config/` (settings, env parsing)
    - `src/db.py` (SQLAlchemy engine/session)
    - `src/email_utils.py` (email backends)
    - backup/restore helpers (if needed)
- `templates/`
  - Jinja templates by role/area.
- `tests/`
  - pytest suite (use in-memory DB in fixtures).
- `docs/`
  - developer + ops + deployment documentation.
- `orga/`
  - macro project planning, task tracking, and domain documentation.
- `.windsurf/`
  - Windsurf runtime rules and workflows.

---

## 3. Development management: orga + tasks

### 3.1 Orga entrypoints

- `orga/README.md` is the entrypoint.
- `orga/tasks/TASKS.md` is the canonical task index.
- `orga/tasks/active/` contains active task folders.
- `orga/tasks/archive/` contains completed task folders.

### 3.2 Task folder format

Each task folder should include:

- `brief.md`
  - Planner-to-task handoff (macro context, scope boundaries, acceptance notes).
- `README.md`
  - Goal and short scope.
- `plan.md`
  - Concrete plan, validation steps, and done criteria.
- Optional `notes.md`
  - Findings, decisions, and progress log.

Canonical location for planner-generated briefs:

- `orga/domain/task-briefs/T-XXX.md`
  - `/project-planner` should create/update these for newly proposed tasks.
  - GitHub Actions **Start Task** copies the canonical brief into the task folder as `brief.md`.

Naming convention:

- `T-XXX-YYYY-MM-DD-short-slug/`

### 3.3 Macro planning

- `orga/domain/project-plan.md` is the macro roadmap.
- Use `/project-planner` to keep it aligned with reality.

---

## 4. Windsurf/Cascade setup: rules + workflows

### 4.1 Runtime vs reference docs

- Runtime rules/workflows live under `.windsurf/`.
- Reference/templates live under `docs/windsurf/` and should stay reasonably aligned.

### 4.2 Active rules used in this repo

The active rules are under `.windsurf/rules/` and are designed to ensure that:

- Work stays traceable in orga docs.
- Commands are safe and reproducible.
- Planning workflows are used consistently.

In this repo, the key rules are:

- `.windsurf/rules/ai-behavior.md`
  - Concise communication.
  - Task workflow discipline (read `TASKS.md`, use task `plan.md`).
  - Command rules:
    - Use `python -m pytest -q`.
    - Do not use `cd` inside commands (set working directory via tooling).
- `.windsurf/rules/project-map.md`
  - Where to find orga docs, code, and templates.
- `.windsurf/rules/task-workflow.md`
  - Task folder naming conventions.
  - Expectation that non-trivial work includes tests + smoke tests.

### 4.3 Workflows used to manage development

The active workflows are under `.windsurf/workflows/` and are invoked in chat using `/workflow-name`.

#### 4.3.1 `/project-planner`

Purpose: keep `orga/domain/project-plan.md` aligned with reality.

What it does (high level):

- Reads `orga/tasks/TASKS.md`.
- Reads `orga/domain/project-plan.md`.
- Reads relevant task `README.md`/`plan.md`/`outcome.md`.
- Uses each task’s `outcome.md` (especially `## Commit / PR references`) as the index from tasks -> commits/PRs -> code.
- Summarizes which phases are active/done and identifies gaps.
- Proposes updates to:
  - `orga/domain/project-plan.md`
    - Includes per-phase task tables (ID/title/status/folder) consistent with `orga/tasks/TASKS.md`.
  - `orga/tasks/TASKS.md` (new tasks, status changes)
- Suggests follow-up work to be planned via `/plan-task`.

When to run:

- Start or completion of a phase.
- When creating a batch of new tasks.
- Regular project health reviews (weekly/bi-weekly).

Output expectations:

- Macro-level changes only (no per-task micro steps).
- Clear “recommended next tasks” list.

#### 4.3.2 `/plan-task`

Purpose: produce a concrete execution plan for one specific task.

What it does (high level):

- Identifies the task ID from context (or requires you to open the task files).
- Reads:
  - `orga/tasks/TASKS.md`
  - The task’s `README.md` and `plan.md` (if present)
- Produces an actionable TODO plan that includes:
  - Analysis/design
  - Implementation
  - Tests + smoke tests (how to validate)
  - Docs updates (when relevant)
- For sensitive work it explicitly asks for:
  - UX review steps
  - permissions/roles mapping
  - threat sketch (security)

Output expectations:

- A small, outcome-oriented TODO list.
- A clear validation section (tests + smoke tests).

### 4.4 docs/windsurf vs .windsurf

- `.windsurf/` is the runtime configuration.
- `docs/windsurf/` is a reference/template that should stay reasonably aligned with `.windsurf/`.

---

## 5. Flask application architecture patterns

### 5.1 App factory

- Use `create_app()` in `app.py`.
- Centralize:
  - configuration (from env)
  - blueprint registration
  - DB initialization
  - security defaults (CSRF, secure cookies in production)
  - health endpoints (`/health`, `/health/db`)

### 5.2 Domain packages

Recommended pattern for each domain area:

- `models.py` – SQLAlchemy models
- `routes.py` – blueprint routes
- `service.py` – business logic and DB access helpers

### 5.3 Email helper

A simple backend switch is usually enough:

- `console` backend: logs messages (safe in dev)
- `memory` backend: in-memory outbox for tests
- `smtp` backend: uses SMTP host/port/user/password from config

---

## 6. Configuration and environment variables

### 6.1 Settings module

Use a dataclass-based `Settings` with `os.getenv(...)` defaults.

### 6.2 Example env file pattern

- Keep `.env` out of git.
- Commit a `.env.example` with:
  - all expected environment variables
  - safe placeholder values (no secrets)

Common variables (adapt names to your project):

- `DATABASE_URL`
- `SECRET_KEY`
- `FLASK_DEBUG`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- Upload controls (optional): `MAX_UPLOAD_SIZE_MB`, `MAX_TOTAL_UPLOAD_SIZE_MB`, `ALLOWED_UPLOAD_MIME_TYPES`
- Email controls: `EMAIL_BACKEND`, `EMAIL_DEFAULT_SENDER`, `EMAIL_SMTP_HOST`, `EMAIL_SMTP_PORT`, `EMAIL_SMTP_USER`, `EMAIL_SMTP_PASSWORD`
- Data root: prefer a single env var (e.g. `APP_DATA_ROOT`); this repo uses `RGS_DATA_ROOT`.

---

## 7. Data handling conventions (data root, uploads, backups)

### 7.1 Data root

- Use a single configurable data root directory.
- In development, default to `<project_root>/data`.
- In production, set it to a durable path like `/srv/<app>/data`.

Typical structure under the data root:

- `uploads/` – user uploaded files
- `backups/`
  - `db_backups/` – DB-only backups
  - `full_backups/` – DB + uploads backups

### 7.2 Backups/restore approach

Recommended baseline:

- Admin Operations page (protected) for:
  - download backup
  - save backup on server
  - restore from uploaded backup
  - restore from server-stored backup
- CLI helper that mirrors the admin logic (useful on servers):
  - `python -m src.backup_save`

---

## 8. Testing and CI conventions

### 8.1 pytest baseline

- All tests under `tests/`.
- Use a fixture to force:
  - `DATABASE_URL=sqlite:///:memory:`
  - safe test admin password
  - test email backend = `memory`

### 8.2 Smoke tests

- Mark critical end-to-end tests with `@pytest.mark.smoke`.
- Commands:
  - `python -m pytest -q`
  - `python -m pytest -m smoke -q`

---

## 9. Deployment model (server) and operations

This repo’s reference deployment pattern:

- App runs in a Proxmox CT (Ubuntu) under systemd.
- TLS and routing handled by a separate nginx CT.
- App is served under a path prefix (example: `/rgsapply/`).

### 9.1 systemd service pattern

- Use a systemd unit that runs the app entrypoint from the venv.
- Keep the service minimal and restart on failure.

### 9.2 nginx reverse proxy with path prefix

If deploying under a prefix:

- Configure nginx to:
  - forward `/prefix/` to the upstream app
  - set `X-Script-Name: /prefix`
- In Flask, use a small WSGI middleware (like `ReverseProxied`) that:
  - reads `X-Script-Name`
  - sets `SCRIPT_NAME`
  - strips the prefix from `PATH_INFO`

### 9.3 Release/update and rollback

A practical baseline:

- Before updating code:
  - create a backup (DB + uploads)
  - record the last-good git commit
- Update code and dependencies
- Restart service
- Run smoke checks:
  - `GET /health`
  - `GET /health/db`
  - one representative core flow

See also:

- `docs/deployment-log.md`
- `docs/deployment-and-release.md`
- `docs/server-update-and-rollback.md`
- `docs/operations-runbook.md`

---

## 10. New project bootstrap checklist (copy/paste)

1. Create repo with baseline structure (`app.py`, `src/`, `templates/`, `tests/`, `docs/`, `orga/`, `.windsurf/`).
2. Add `.windsurf/rules/*` and `.windsurf/workflows/*`.
3. Create `orga/tasks/TASKS.md` and seed your first task(s).
4. Implement:
   - `create_app()`
   - config (`src/config/settings.py`)
   - DB initialization (`src/db.py`)
   - health endpoints
5. Add `.env.example` and ensure `.env` is gitignored.
6. Create a minimal test suite and ensure `python -m pytest -q` passes.
7. Write ops docs early:
   - operations runbook
   - deployment/release steps
   - rollback routine
8. Deploy:
   - systemd service
   - nginx reverse proxy (optional prefix)
   - persistent `DATA_ROOT`
   - smoke checks
