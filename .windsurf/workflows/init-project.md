---
description: Initialize a new project (interactive)
auto_execution_mode: 0
---


# /init-project – Interactive project initialization

Goal: Gather the project’s essential context interactively (asking follow-up questions until the picture is complete) and generate a structured project brief and baseline docs.

## Quick path (recommended)

- Gather enough context to write `orga/domain/project-brief.md` (users/roles, key flows, data sensitivity, threats, tech choices).
- Generate baseline domain docs (`requirements.md`, `architecture.md`, `data-model.md`, `project-plan.md`).
- Record evidence in `orga/domain/init-run.md`.
- Ensure `orga/tasks/TASKS.md` and a first task folder exist.
- End with the wrap-up gate (git status + commit decision).

## Outputs (files to create/update)

- `orga/domain/project-brief.md` (primary AI-ready summary)
- `orga/domain/requirements.md` (first cut)
- `orga/domain/architecture.md` (first cut)
- `orga/domain/data-model.md` (first cut)
- `orga/domain/project-plan.md` (initial milestones/phases)
- `orga/domain/project-planner-handoff.md` (what to do next + inputs to prepare)
- `orga/domain/task-briefs/` (canonical planner-to-task handoff briefs, one per task)
- `orga/domain/init-run.md` (init checklist ledger and evidence)
- `orga/tasks/TASKS.md` and `orga/tasks/active/T-001-YYYY-MM-DD-initial-setup/` (required unless explicitly skipped)
- `docs/windsurf/skills/*` (project-specific skills)
- `.gitignore` (baseline hygiene for private files and local artifacts)
- `.env.example` (optional: document required environment variables without secrets)
- `.env` (local-only: created from `.env.example`, never committed)

## 1) Gather context (interactive) (detailed prompts)

Ask the user questions until the following sections are complete. If information is missing, keep asking, but keep questions concise and grouped.

1) Project identity
- Project name
- One-sentence purpose
- Primary users / stakeholders

2) Domain and scope
- Core user journeys (top 3)
- Out of scope (explicit)
- Non-functional requirements (availability, performance, privacy)

3) Data
- Entities (rough list)
- Data sensitivity (PII, credentials, payments)
- Storage preferences (SQL/NoSQL/files)

Privacy & security prompts (must ask)

- What data is **private/sensitive** (PII, credentials, student data, HR, health, payments)?
- What must never be committed to git (API keys, `.env`, DB dumps, uploads, exports)?
- Any compliance constraints (GDPR, retention, deletion requests)?
- Authentication/authorization expectations (roles, permissions boundaries)?
- Threat hotspots (file uploads, admin panels, webhooks, token links, data exports)?

4) Interfaces
- UI type (web, mobile, CLI)
- APIs/integrations (auth provider, email, payments, etc.)

5) Tech choices (if known)
- Language/runtime
- Framework
- DB
- Deployment target (local only, Docker, VPS, cloud)

6) Quality & delivery
- Testing expectations (unit/integration/e2e)
- CI expectations
- Security posture (roles/permissions, threat hotspots)

## 2) Produce a structured project brief

Write `orga/domain/project-brief.md` as a concise, AI-optimized checklist-style reference. Use headings and bullet lists.

Suggested structure:

- Overview
- Users & roles
- Key flows
- Data model sketch
- External integrations
- Constraints & non-goals
- Quality gates (tests, lint, CI)
- Security notes
- Open questions

## 3) Seed baseline domain docs

From the brief, generate a first-cut version of:

- `requirements.md` (key requirements + acceptance hints)
- `architecture.md` (high-level components + boundaries)
- `data-model.md` (entities + relationships)
- `project-plan.md` (phases/milestones + suggested tasks)

Keep these lightweight; they will evolve.

Also ensure the docs explicitly capture privacy/security:

- In `orga/domain/project-brief.md` include:
  - data sensitivity classification
  - roles/permissions sketch
  - threat hotspots

## 4) Create project-specific Windsurf customizations (required unless explicitly skipped)

Create or update a small set of project-specific files under `docs/windsurf/` so future Cascade sessions are guided by project-tailored instructions.

1) Skills

- Ensure `docs/windsurf/skills/` exists.
- Add or update a project onboarding skill (name it using lowercase letters/numbers/hyphens) that:
  - points at `orga/domain/project-brief.md`
  - lists the project’s key flows and roles
  - describes the preferred dev/test commands for this repo

2) Rules (only if needed)

- Prefer keeping shared behavior rules generic.
- If the project needs special constraints (security posture, data handling, allowed tools), add a new rule file under `docs/windsurf/rules/` rather than modifying the shared rules.

3) Workflows (only if needed)

- If the project needs a repeatable procedure, add a workflow under `docs/windsurf/workflows/`.
- Keep workflows short and outcome-oriented.

4) Repo hygiene artifacts

- Create or update `.gitignore` with at least:
  - `.venv/`, `__pycache__/`, `*.pyc`
  - `.env`
  - OS/editor artifacts (e.g. `.DS_Store`)
- If the project uses file uploads or local data roots, add a clear ignore pattern for them.
- If environment variables are required, create `.env.example` with placeholder values and no secrets.

If `.env.example` exists, also create a local `.env` from it and fill in the required values. Ensure `.env` remains uncommitted.

Also record completion of this step in `orga/domain/init-run.md`.

## 5) Initialize tasks (required unless explicitly skipped)

If the repo does not yet have a task index, create:

- `orga/tasks/TASKS.md` with `T-001` as the first active task.
- `orga/tasks/active/T-001-YYYY-MM-DD-initial-setup/README.md`
- `orga/tasks/active/T-001-YYYY-MM-DD-initial-setup/plan.md`

Also ensure `T-001/plan.md` contains a checked-step ledger for `/init-project` (step list + done/skipped + evidence paths).

## 6) Reminder

If you changed any runtime Windsurf files under `.windsurf/`, update `docs/windsurf/` too and tell the user to copy/sync (see `docs/windsurf/SYNC.md`).

## 7) Optional: environment bootstrap (recommended)

If this is a Python project, recommend creating a virtual environment and capturing the expected commands:

- `python -m venv .venv`
- `python -m pip install --upgrade pip`
- If present: `python -m pip install -r requirements.txt`
- Tests: `python -m pytest -q`

Ensure `.venv/` is in `.gitignore`.

## 8) Wrap up: make the initialization “real”

End with a clear end state (mandatory unless explicitly skipped):

- Run `git status --porcelain` and summarize what changed.
- Commit with a standard message (e.g. `chore: initialize project`) or explicitly record why no commit is being made.
- Push (or instruct the user to push).
- If the repo uses PR-based flow, recommend opening a PR.

Optional (no GitHub UI clicks): if the user prefers PR-based initialization via GitHub Actions, dispatch the mechanical init workflow locally:

- `python .github/scripts/dispatch_workflow.py --workflow init-project.yml --ref main --input project_name="..." --input init_tasks=true --input purge_legacy_tasks=true --input purge_docs=true --input force=false --input auto_merge=true`

Clarify:

- This `/init-project` workflow is local and interactive.
- The GitHub Actions workflow **Initialize Project** is mechanical and applies changes via PR.

## 9) Next: macro planning

Generate or update `orga/domain/project-planner-handoff.md` and recommend running `/project-planner` next (before detailed per-task `/plan-task`).
