# Sync policy: `docs/windsurf` <-> `.windsurf`

`docs/windsurf/` is the **copy-ready reference pack** for Windsurf/Cascade customization.

- Runtime files live under `.windsurf/`.
- Reference/copy files live under `docs/windsurf/`.

## Canonical source (recommended)

Treat `docs/windsurf/` as the **canonical source** you keep tidy and copy from. This avoids drift and makes it easy to bootstrap new repos.

## Required workflow when Windsurf files change

Whenever you change any of these:

- `.windsurf/rules/*`
- `.windsurf/workflows/*`
- `.windsurf/skills/*`

You must also:

- Update the corresponding files in `docs/windsurf/`.
- Notify the maintainer to copy/sync `docs/windsurf/` into `.windsurf/`.

This requirement is also encoded in `docs/windsurf/rules/ai-behavior.md`.

## Copy procedure (manual)

Copy these directories:

- `docs/windsurf/rules/` -> `.windsurf/rules/`
- `docs/windsurf/workflows/` -> `.windsurf/workflows/`
- `docs/windsurf/skills/` -> `.windsurf/skills/`

Recommended approach: delete/overwrite the target files so runtime exactly matches the reference pack.

## Optional: keep a checklist in PRs

When a change touches Windsurf configuration, include a short note in the PR description:

- Updated: `.windsurf/...`
- Updated: `docs/windsurf/...`
- Action required: copy `docs/windsurf` -> `.windsurf` in any downstream repos using this pack
