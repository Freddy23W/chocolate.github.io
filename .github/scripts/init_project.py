from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Inputs:
    project_name: str
    init_tasks: bool
    purge_legacy_tasks: bool
    purge_docs: bool
    force: bool


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    raw = raw.strip().lower()
    if raw in {"1", "true", "yes", "y", "on"}:
        return True
    if raw in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"Invalid boolean env var {name}={raw!r}")


def load_inputs() -> Inputs:
    project_name = (os.environ.get("PROJECT_NAME") or "").strip()
    if not project_name:
        raise ValueError("PROJECT_NAME is required")

    return Inputs(
        project_name=project_name,
        init_tasks=_env_bool("INIT_TASKS", True),
        purge_legacy_tasks=_env_bool("PURGE_LEGACY_TASKS", False),
        purge_docs=_env_bool("PURGE_DOCS", False),
        force=_env_bool("FORCE", False),
    )


def rm_tree(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists() or not src.is_dir():
        raise ValueError(f"Source directory does not exist: {src}")

    ensure_dir(dst)

    for root, dirs, files in os.walk(src):
        root_path = Path(root)
        rel = root_path.relative_to(src)
        target_root = dst / rel
        ensure_dir(target_root)

        for d in dirs:
            ensure_dir(target_root / d)

        for f in files:
            s = root_path / f
            t = target_root / f
            shutil.copy2(s, t)


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_text_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    write_text(path, content)
    return True


def _ensure_tasks_dirs_if_index_exists(repo_root: Path) -> None:
    tasks_dir = repo_root / "orga" / "tasks"
    tasks_index = tasks_dir / "TASKS.md"
    if not tasks_index.exists():
        return

    ensure_dir(tasks_dir / "active")
    ensure_dir(tasks_dir / "archive")
    write_text_if_missing(tasks_dir / "active" / ".gitkeep", "")
    write_text_if_missing(tasks_dir / "archive" / ".gitkeep", "")


def main() -> None:
    repo_root = Path.cwd()
    inputs = load_inputs()

    marker = repo_root / ".github" / ".project_initialized"
    if marker.exists() and not inputs.force:
        raise SystemExit(
            "Repository appears already initialized (.github/.project_initialized exists). "
            "Re-run with FORCE=true if you really want to apply again."
        )

    docs_windsurf = repo_root / "docs" / "windsurf"
    runtime_windsurf = repo_root / ".windsurf"

    project_brief_path = repo_root / "orga" / "domain" / "project-brief.md"
    has_project_brief = project_brief_path.exists()

    if inputs.purge_docs:
        docs_dir = repo_root / "docs"
        if docs_dir.exists():
            for child in docs_dir.iterdir():
                if child.name == "windsurf":
                    continue
                rm_tree(child)

    if inputs.purge_legacy_tasks:
        tasks_dir = repo_root / "orga" / "tasks"
        rm_tree(tasks_dir / "active")
        rm_tree(tasks_dir / "archive")
        ensure_dir(tasks_dir / "active")
        ensure_dir(tasks_dir / "archive")
        write_text(tasks_dir / "archive" / ".gitkeep", "")

    _ensure_tasks_dirs_if_index_exists(repo_root)

    copy_tree(docs_windsurf / "rules", runtime_windsurf / "rules")
    copy_tree(docs_windsurf / "workflows", runtime_windsurf / "workflows")
    skills_src = docs_windsurf / "skills"
    if skills_src.exists():
        copy_tree(skills_src, runtime_windsurf / "skills")

    readme_content = f"# {inputs.project_name}\n\n" "This repository was initialized from a template.\n"
    if has_project_brief:
        readme_content += "\n## Project brief\n\n- `orga/domain/project-brief.md`\n"

    gitignore_content = (
        ".env\n"
        ".env.*\n"
        "!.env.example\n"
        ".venv/\n"
        "venv/\n"
        "__pycache__/\n"
        "*.pyc\n"
        ".pytest_cache/\n"
        ".mypy_cache/\n"
        ".ruff_cache/\n"
        ".coverage\n"
        "htmlcov/\n"
        "dist/\n"
        "build/\n"
        "*.egg-info/\n"
        ".DS_Store\n"
        "Thumbs.db\n"
        ".idea/\n"
        ".vscode/\n"
    )
    if inputs.force:
        write_text(repo_root / ".gitignore", gitignore_content)
    else:
        write_text_if_missing(repo_root / ".gitignore", gitignore_content)

    if inputs.force:
        write_text(repo_root / "README.md", readme_content)
    else:
        write_text_if_missing(repo_root / "README.md", readme_content)

    ensure_dir(repo_root / "orga")
    orga_readme = repo_root / "orga" / "README.md"
    orga_readme_content = (
        "# Project Orga\n\n"
        "This folder collects all **non-code project organization** for this repository.\n\n"
        "## Start here\n\n"
        "- `tasks/TASKS.md` – overview of active/backlog/archived tasks.\n"
        "- `tasks/active/` – current task folders (one folder per task).\n"
        "- `tasks/archive/` – completed tasks and their notes.\n"
        "- `domain/` – domain and architecture notes (requirements, data model, architecture, project plan).\n"
        "- `../docs/windsurf/` – template/reference for AI/Windsurf rules and workflows (active ones live under `.windsurf/`).\n"
        "\n"
        "Note: `orga/_legacy/` contains reference/example content from earlier work. New projects should track current work under `orga/tasks/active/`.\n"
    )
    if inputs.force:
        write_text(orga_readme, orga_readme_content)
    else:
        write_text_if_missing(orga_readme, orga_readme_content)

    domain_dir = repo_root / "orga" / "domain"
    ensure_dir(domain_dir)

    task_briefs_dir = domain_dir / "task-briefs"
    ensure_dir(task_briefs_dir)
    write_text_if_missing(task_briefs_dir / ".gitkeep", "")

    if inputs.force:
        write_text(domain_dir / "project-plan.md", "# Project plan\n")
        write_text(domain_dir / "requirements.md", "# Requirements\n")
        write_text(domain_dir / "architecture.md", "# Architecture\n")
        write_text(domain_dir / "data-model.md", "# Data model\n")
    else:
        write_text_if_missing(domain_dir / "project-brief.md", "# Project brief\n")
        write_text_if_missing(domain_dir / "project-plan.md", "# Project plan\n")
        write_text_if_missing(domain_dir / "requirements.md", "# Requirements\n")
        write_text_if_missing(domain_dir / "architecture.md", "# Architecture\n")
        write_text_if_missing(domain_dir / "data-model.md", "# Data model\n")
        write_text_if_missing(domain_dir / "project-planner-handoff.md", "# Project-planner handoff\n")
        write_text_if_missing(
            domain_dir / "init-run.md",
            "# Init run ledger\n\n"
            "## Checklist\n\n"
            "- [ ] Step 1: Gather context\n"
            "- [ ] Step 2: Produce `orga/domain/project-brief.md`\n"
            "- [ ] Step 3: Seed baseline domain docs\n"
            "- [ ] Step 4: Create project-specific Windsurf customizations\n"
            "- [ ] Step 4b: Create local `.env` from `.env.example` (never commit `.env`)\n"
            "- [ ] Step 5: Initialize tasks (`T-001`)\n"
            "- [ ] Step 8: Wrap up (git status + commit decision)\n\n"
            "## Evidence\n\n"
            "- Project brief: \n"
            "- Domain docs: \n"
            "- Task folder(s): \n"
            "- Windsurf customizations: \n"
            "- Env: created `.env` from `.env.example`\n"
            "- Git status: \n"
            "- Commit:\n",
        )

    if inputs.init_tasks:
        tasks_dir = repo_root / "orga" / "tasks"
        ensure_dir(tasks_dir / "active")
        ensure_dir(tasks_dir / "archive")

        tasks_index_content = (
            "# Tasks\n\n"
            "This file tracks tasks and links them to their folders.\n\n"
            "Status values: `backlog`, `active`, `done`.\n\n"
            "| ID    | Title                 | Status | Folder                                              |\n"
            "|-------|-----------------------|--------|-----------------------------------------------------|\n"
            "| T-001 | Initial setup         | active | orga/tasks/active/T-001-YYYY-MM-DD-initial-setup/   |\n"
        )
        if inputs.force:
            write_text(tasks_dir / "TASKS.md", tasks_index_content)
        else:
            write_text_if_missing(tasks_dir / "TASKS.md", tasks_index_content)

        t1_dir = tasks_dir / "active" / "T-001-YYYY-MM-DD-initial-setup"
        ensure_dir(t1_dir)
        write_text(
            t1_dir / "brief.md",
            "# Task brief: T-001 Initial setup\n\n"
            "## Context (from project planner)\n\n"
            "- This task is the durable checklist for initialization and bootstrapping.\n\n"
            "## Intended outcome\n\n"
            "- The repository is initialized and ready for macro planning and task execution.\n\n"
            "## Scope boundaries\n\n"
            "In:\n"
            "- Initialization, baseline docs, workflow setup\n\n"
            "Out:\n"
            "- Feature development\n\n"
            "## Acceptance notes\n\n"
            "- Init checklist completed and recorded\n\n"
            "## Dependencies / prerequisites\n\n"
            "- None\n\n"
            "## Key paths / artifacts\n\n"
            "- orga/domain/project-brief.md\n"
            "- orga/domain/init-run.md\n"
            "- orga/tasks/TASKS.md\n",
        )
        write_text(
            t1_dir / "README.md",
            "# T-001 Initial setup\n\n"
            "Status: active\n"
            "Created: YYYY-MM-DD\n\n"
            "## Goal\n\n"
            "- Establish the baseline structure, tooling, and documentation for the project.\n\n"
            "## Scope\n\n"
            "In:\n"
            "- \n\n"
            "Out:\n"
            "- \n\n"
            "## Acceptance criteria\n\n"
            "- \n\n"
            "## Links\n\n"
            "- brief.md\n"
            "- orga/domain/project-brief.md\n"
            "- orga/domain/requirements.md\n"
            "- orga/domain/architecture.md\n"
            "- orga/domain/data-model.md\n\n"
            "## Open questions / risks\n\n"
            "- \n",
        )
        write_text(
            t1_dir / "plan.md",
            "# Plan\n\n"
            "## Init checklist ledger (/init-project)\n\n"
            "- [ ] Step 1: Gather context\n"
            "- [ ] Step 2: Produce `orga/domain/project-brief.md`\n"
            "- [ ] Step 3: Seed baseline domain docs\n"
            "- [ ] Step 4: Create project-specific Windsurf customizations\n"
            "- [ ] Step 5: Initialize tasks (`T-001`)\n"
            "- [ ] Step 8: Wrap up (git status + commit decision)\n\n"
            "## Steps\n\n"
            "1. Define scope and core requirements\n"
            "2. Establish development workflow (tasks, branches, CI)\n"
            "3. Add minimal app skeleton\n"
            "4. Add tests and a smoke-test path\n\n"
            "## Validation plan\n\n"
            "Automated tests:\n"
            "- \n\n"
            "Smoke checks:\n"
            "- \n\n"
            "## Progress log\n\n"
            "- YYYY-MM-DD: \n\n"
            "## Decisions\n\n"
            "- \n",
        )
        write_text(
            t1_dir / "outcome.md",
            "# Outcome\n\n"
            "## Summary of changes\n\n"
            "- \n\n"
            "## Rationale / decisions\n\n"
            "- \n\n"
            "## Scope boundaries\n\n"
            "In:\n"
            "- \n\n"
            "Out:\n"
            "- \n\n"
            "## Validation\n\n"
            "Tests run:\n"
            "- \n\n"
            "Smoke checks:\n"
            "- \n\n"
            "## Artifacts / paths\n\n"
            "- \n\n"
            "## Follow-ups\n\n"
            "- \n",
        )

    write_text(marker, "initialized\n")

    print("Initialization complete.")
    print("- Synced docs/windsurf -> .windsurf")
    if inputs.purge_docs:
        print("- Purged docs/* except docs/windsurf")
    if inputs.purge_legacy_tasks:
        print("- Purged orga/tasks/active and orga/tasks/archive")
    if inputs.init_tasks:
        print("- Initialized orga/tasks/TASKS.md and created T-001")


if __name__ == "__main__":
    main()
