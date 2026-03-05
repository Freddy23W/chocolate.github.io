# GitHub Actions setup (required for template workflows)

This template provides GitHub Actions workflows that create branches and open pull requests.

The following workflows require **write** permissions:

- `Initialize Project` (`.github/workflows/init-project.yml`)
- `Start Task` (`.github/workflows/start-task.yml`)
- `Finish Task` (`.github/workflows/finish-task.yml`)

They use the repository-provided `GITHUB_TOKEN` (no PAT required).

## Branchless / local-commit mode (single maintainer)

For a single maintainer working primarily on the default branch (often `main`), you can run this template in a **branchless / local-commit** mode:

- You may choose **not** to use the **Start Task** / **Finish Task** workflows for every task (or at all).
- Instead, create and update task folders and docs directly on your working branch (`orga/tasks/active/...`), commit changes locally, and record the relevant commit hashes in each task’s `outcome.md` under `## Commit / PR references`.
- The workflows described in this document are **optional helpers** for PR-based automation and repo hygiene; they are not required for the template to function.

Typical branchless setup:

- Use **Initialize Project** once to scaffold the repo (optional but recommended).
- Work directly on `main`, using `/plan-task` and `/work-on-task` to drive task execution and keep `plan.md` / `outcome.md` up to date.
- Use dedicated PRs (with or without these workflows) only for larger or riskier changes, or when collaborating.

## Optional: dispatch workflows without GitHub UI (Windsurf/local)

If you want to avoid clicking “Run workflow” in GitHub, you can dispatch the template workflows locally via the GitHub API:

- Script: `.github/scripts/dispatch_workflow.py`
- Example env template: `.env.example`

This requires a token available to your local environment.

Recommended:

- Set `GH_TOKEN` in your local `.env` (do not commit it).

Token permissions (fine-grained PAT recommended):

- Actions: Read and write (to dispatch workflow runs)
- Contents: Read and write
- Pull requests: Read and write

Notes:

- The GitHub Actions workflows themselves still run with `GITHUB_TOKEN` (or `GH_PR_TOKEN` if configured).
- This script only triggers `workflow_dispatch`; it does not create commits locally.

Examples:

- Initialize Project:
  - `python .github/scripts/dispatch_workflow.py --workflow init-project.yml --ref main --input project_name="My Project" --input init_tasks=true --input purge_legacy_tasks=true --input purge_docs=true --input force=false`
- Start Task:
  - `python .github/scripts/dispatch_workflow.py --workflow start-task.yml --ref main --input task_id=T-002 --input title="Short title" --input auto_merge=true --input delete_branch=false`
- Finish Task:
  - `python .github/scripts/dispatch_workflow.py --workflow finish-task.yml --ref main --input task_id=T-002 --input auto_merge=true`

Note: `auto_merge=true` requires the repo setting **Allow auto-merge** and typically branch protection rules (required checks and/or reviews).

## Required repository settings

1) Ensure workflows are on the default branch

- GitHub only allows manual `workflow_dispatch` runs for workflow files that exist on the repository’s **default branch**.

2) Actions must be enabled

- Repository settings -> **Actions** -> **General**.
- Ensure GitHub Actions are enabled for the repo (and allowed by your org policy).

3) Workflow permissions (critical)

- Repository settings -> **Actions** -> **General** -> **Workflow permissions**
  - Select **Read and write permissions**.

These workflows also explicitly request:

- `permissions: contents: write`
- `permissions: pull-requests: write`

4) Marketplace actions must be allowed

These workflows use:

- `peter-evans/create-pull-request@v6`

If your org restricts third-party actions, you must allow this action (or we can replace it with `actions/github-script` + REST API).

## Optional: auto-merge for workflow-created PRs

Some template workflows can optionally enable GitHub auto-merge on the PR they create.

Prerequisites:

- Repository settings -> Pull Requests:
  - Enable **Allow auto-merge**.
- Branch protection on the default branch should require at least one check or review.

Recommended setup:

- Add a required status check for your default branch (for example, the `CI` workflow in this template).

Notes:

- Auto-merge only merges when requirements are satisfied.
- Whether tests run "again" after merge depends on your CI configuration. If you have a workflow that runs on `push` to `main`, it will run post-merge.

## If PR creation is blocked (common)

Some repositories/orgs block PR creation via `GITHUB_TOKEN`. In that case you may see an error like:

"GitHub Actions is not permitted to create or approve pull requests."

Fix options:

1) Enable PR creation for Actions (preferred)

- Repository settings -> **Actions** -> **General** -> **Workflow permissions**
  - Enable **Allow GitHub Actions to create and approve pull requests**

2) Use a dedicated token secret (fallback)

- Create a fine-grained PAT (or org-approved token) with at least:
  - Contents: Read and write
  - Pull requests: Read and write
- Add it as a repository secret named `GH_PR_TOKEN`.

This template’s workflows support `GH_PR_TOKEN` automatically when present.

## Notes on branch protection

- It’s fine (and recommended) to protect `main` with “Require PR reviews” or required checks.
- These workflows open PRs; they do not push directly to `main`.

## Notes

- If you enable "create and approve", workflows can also approve PRs. This template does not auto-approve anything; it only creates PRs.
