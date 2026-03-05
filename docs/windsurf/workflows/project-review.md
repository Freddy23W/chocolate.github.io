---
description: Project-wide critical review workflow
auto_execution_mode: 0
---

# /project-review – Project-wide critical review workflow

Goal: Run a deep, critical audit of the current system and turn findings into concrete follow-up tasks.

## When to run this workflow

- At the end of a major phase.
- Before important milestones (e.g. a production deployment or major refactor).
- When you suspect drift between implementation, domain requirements, and documentation.

## 1) Gather context

1. Read the **macro docs** (if they exist):
   - `orga/domain/project-plan.md`.
   - `orga/domain/requirements.md`.
   - `orga/domain/data-model.md`.
   - `orga/domain/architecture.md`.
2. Review recent **review tasks** and their notes (especially the latest ones).
3. Scan `docs/` for key entrypoints (adapt to your project):
   - `docs/getting-started.md`.
   - `docs/developer-guide.md`.
   - `docs/testing-and-ci.md`.
   - Any ops/admin/user docs relevant to your domain.

## 2) Run automated checks

1. Run the full test suite:
   - `python -m pytest -q`
2. Run smoke tests only (optional quick check):
   - `python -m pytest -m smoke -q`
3. Note:
   - Any failing tests.
   - Warnings related to domain logic, time handling, deprecations, configuration, or security.

## 3) Manual & structural review

1. **Primary user flow(s)**
   - Start from the main entrypoints.
   - Exercise the core happy path(s) end-to-end.
   - Exercise at least one important error path (invalid input, missing permissions, expired token, etc.).

2. **Secondary/adjacent flow(s)**
   - Exercise supporting flows (e.g. notifications, uploads, exports, dashboards) that are easy to break.

3. **Permissions/roles** (if applicable)
   - Verify who can see/do what.
   - Attempt at least one manual “attack” (try to access privileged routes or objects).

4. **Operations & environment** (if applicable)
   - Cross-check environment variables/defaults against ops docs.
   - Verify operational guardrails (backups, logging, monitoring, retention) if present.

## 4) Summarize findings

In the active review task’s `notes.md`, record:

- **Domain gaps**
  - Missing or mismatched requirements/fields/flows.
- **Code & architecture issues**
  - Divergence from documented architecture.
  - Complexity hotspots.
- **Testing gaps**
  - Critical flows not covered.
  - Negative/error paths without coverage.
- **Docs & workflows**
  - Out-of-date or confusing docs.
  - Workflow friction.
- **Ops & readiness**
  - Risks around config, access control, retention, backups, or monitoring.

Keep notes in concise bullet lists with headings.

## 5) Create follow-up tasks

Based on findings:

1. For each significant gap/risk, create a new task in `orga/tasks/TASKS.md` and plan it with `/plan-task`.
2. For small issues that don’t warrant a full task, either:
   - Fix directly if low-risk and unambiguous, or
   - Group into a single cleanup task.

## 6) Completion criteria

You can consider the `/project-review` run complete when:

- Automated tests (and smoke tests if used) have been run and results are noted.
- Manual checks of the main flows have been performed.
- Findings and risks are recorded under clear headings.
- Follow-up tasks exist for the most important gaps.
