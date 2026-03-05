# Windsurf/Cascade Rules, Workflows, and Skills

This folder contains **templates and documentation** for project-specific rules, workflows, and skills for Cascade in this repo.

Runtime activation:

- The **active** rules, workflows, and skills used by Windsurf live under `.windsurf/` in this repo.
- This `docs/windsurf` folder is a template/reference; keep it reasonably in sync with `.windsurf` when rules, workflows, or skills change, especially for UX, permissions/roles, and security-related quality gates.
- See `docs/windsurf/SYNC.md` for the required copy/sync procedure.

This reference pack includes a workflow completion enforcement rule:

- `docs/windsurf/rules/workflow-execution-protocol.md`

To activate it in another repo, copy/sync `docs/windsurf/` -> `.windsurf/`.

Naming conventions:

- Rules: `*.md` with an optional front matter `trigger` (e.g., `always_on`).
- Workflows: `*.md` invoked as `/filename` (without extension) inside Cascade.
- Skills: folders under `skills/<skill-name>/` containing a `SKILL.md` with front matter `name` and `description`.

## Command execution & tests

- Commands issued by Cascade **must be valid shell commands**, without prompts or directory prefixes.
- The AI never uses `cd` inside commands; instead, tools set the working directory (Cwd) to the repo root.
- Maintainers should ensure that:
  - `python` on PATH points at the project’s virtual environment (or a suitable interpreter), **or** they consistently use `py -m pytest` and document this in task plans.
- These conventions are mirrored in `docs/windsurf/rules/ai-behavior.md` and should be kept in sync with the active rules under `.windsurf/`.
