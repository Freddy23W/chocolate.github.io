from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Inputs:
    task_id: str
    title: str
    slug: str
    date: str
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


def _sanitize_task_id(task_id: str) -> str:
    task_id = task_id.strip().upper()
    if not re.fullmatch(r"T-\d{3}", task_id):
        raise ValueError("TASK_ID must look like T-002")
    return task_id


def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "task"


def _sanitize_slug(slug: str) -> str:
    slug = slug.strip().lower()
    if not slug:
        return slug
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("TASK_SLUG must contain only lowercase letters/numbers/hyphens")
    return slug


def _sanitize_date(date_s: str) -> str:
    date_s = date_s.strip()
    if not date_s:
        return date_s
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_s):
        raise ValueError("TASK_DATE must be YYYY-MM-DD")
    return date_s


def load_inputs() -> Inputs:
    task_id = _sanitize_task_id(os.environ.get("TASK_ID", ""))
    title = (os.environ.get("TASK_TITLE") or "").strip()
    if not title:
        raise ValueError("TASK_TITLE is required")

    slug_in = _sanitize_slug(os.environ.get("TASK_SLUG") or "")
    slug = slug_in if slug_in else _slugify(title)

    date_in = _sanitize_date(os.environ.get("TASK_DATE") or "")
    date = date_in if date_in else datetime.now(timezone.utc).strftime("%Y-%m-%d")

    force = _env_bool("FORCE", False)

    return Inputs(task_id=task_id, title=title, slug=slug, date=date, force=force)


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_text(p: Path, content: str) -> None:
    ensure_dir(p.parent)
    p.write_text(content, encoding="utf-8", newline="\n")


def append_tasks_md(tasks_md: Path, task_id: str, title: str, folder: str, status: str = "active") -> None:
    if not tasks_md.exists():
        raise FileNotFoundError(f"Missing {tasks_md}")

    existing = tasks_md.read_text(encoding="utf-8")
    if re.search(rf"\|\s*{re.escape(task_id)}\s*\|", existing):
        raise ValueError(f"TASKS.md already contains an entry for {task_id}")

    row = f"| {task_id} | {title} | {status} | {folder} |\n"

    content = existing
    if not content.endswith("\n"):
        content += "\n"

    content += row
    tasks_md.write_text(content, encoding="utf-8", newline="\n")


def write_github_output(**kv: str) -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        return
    with open(out_path, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def main() -> None:
    repo_root = Path.cwd()
    inp = load_inputs()

    tasks_md = repo_root / "orga" / "tasks" / "TASKS.md"
    if not tasks_md.exists():
        raise SystemExit("Missing orga/tasks/TASKS.md. Initialize the project first.")

    folder_name = f"{inp.task_id}-{inp.date}-{inp.slug}"
    folder_rel = f"orga/tasks/active/{folder_name}/"
    task_dir = repo_root / "orga" / "tasks" / "active" / folder_name

    if task_dir.exists():
        raise SystemExit(f"Task folder already exists: {folder_rel}")

    ensure_dir(task_dir)

    canonical_brief = repo_root / "orga" / "domain" / "task-briefs" / f"{inp.task_id}.md"
    if canonical_brief.exists():
        brief_content = canonical_brief.read_text(encoding="utf-8")
    else:
        brief_content = (
            f"# Task brief: {inp.task_id} {inp.title}\n\n"
            "## Context (from project planner)\n\n"
            "- \n\n"
            "## Intended outcome\n\n"
            "- \n\n"
            "## Scope boundaries\n\n"
            "In:\n"
            "- \n\n"
            "Out:\n"
            "- \n\n"
            "## Acceptance notes\n\n"
            "- \n\n"
            "## Dependencies / prerequisites\n\n"
            "- \n\n"
            "## Key paths / artifacts\n\n"
            "- \n"
        )

    readme_content = (
        f"# {inp.task_id} {inp.title}\n\n"
        "Status: active\n"
        f"Created: {inp.date}\n\n"
        "## Goal\n\n"
        "- \n\n"
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
        "- \n"
    )
    plan_content = (
        "# Plan\n\n"
        "## Steps\n\n"
        "1. \n\n"
        "## Validation plan\n\n"
        "Automated tests:\n"
        "- \n\n"
        "Smoke checks:\n"
        "- \n\n"
        "## Progress log\n\n"
        f"- {inp.date}: created task scaffold\n\n"
        "## Decisions\n\n"
        "- \n"
    )
    outcome_content = (
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
        "## Commit / PR references\n\n"
        "- Commit(s): \n"
        "- PR: \n\n"
        "## Follow-ups\n\n"
        "- \n"
    )

    write_text(
        task_dir / "brief.md",
        brief_content,
    )
    write_text(
        task_dir / "README.md",
        readme_content,
    )
    write_text(
        task_dir / "plan.md",
        plan_content,
    )
    write_text(
        task_dir / "outcome.md",
        outcome_content,
    )

    try:
        append_tasks_md(tasks_md, inp.task_id, inp.title, folder_rel)
    except ValueError:
        if inp.force:
            pass
        else:
            raise

    branch = f"task/{inp.task_id.lower()}-{inp.slug}"
    pr_title = f"{inp.task_id}: {inp.title}"
    commit_message = f"Start {inp.task_id}: {inp.title}"

    write_github_output(branch=branch, pr_title=pr_title, commit_message=commit_message, task_folder=folder_rel)


if __name__ == "__main__":
    main()
