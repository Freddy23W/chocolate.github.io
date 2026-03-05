from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Inputs:
    task_id: str
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


def load_inputs() -> Inputs:
    task_id = _sanitize_task_id(os.environ.get("TASK_ID", ""))
    force = _env_bool("FORCE", False)
    return Inputs(task_id=task_id, force=force)


def write_github_output(**kv: str) -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        return
    with open(out_path, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def find_active_task_folder(repo_root: Path, task_id: str) -> Path:
    active_dir = repo_root / "orga" / "tasks" / "active"
    if not active_dir.exists():
        raise FileNotFoundError("Missing orga/tasks/active")

    matches = [p for p in active_dir.iterdir() if p.is_dir() and p.name.startswith(f"{task_id}-")]
    if not matches:
        raise FileNotFoundError(f"No active task folder found for {task_id} under orga/tasks/active")
    if len(matches) > 1:
        names = ", ".join(p.name for p in matches)
        raise RuntimeError(f"Multiple active task folders match {task_id}: {names}")
    return matches[0]


def update_tasks_index(tasks_md: Path, task_id: str, new_folder_rel: str, force: bool) -> None:
    if not tasks_md.exists():
        if force:
            return
        raise FileNotFoundError(f"Missing {tasks_md}")

    lines = tasks_md.read_text(encoding="utf-8").splitlines(True)
    updated = False

    for i, line in enumerate(lines):
        if re.search(rf"\|\s*{re.escape(task_id)}\s*\|", line):
            parts = [p.strip() for p in line.strip("\n").split("|")]
            # parts looks like: ["", "T-001", "Title", "active", "folder", ""]
            if len(parts) < 6:
                if force:
                    return
                raise ValueError(f"Unexpected TASKS.md row format for {task_id}: {line!r}")

            tid = parts[1]
            title = parts[2]
            lines[i] = f"| {tid} | {title} | done | {new_folder_rel} |\n"
            updated = True
            break

    if not updated and not force:
        raise ValueError(f"TASKS.md has no row for {task_id}")

    if updated:
        tasks_md.write_text("".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    repo_root = Path.cwd()
    inp = load_inputs()

    active_folder = find_active_task_folder(repo_root, inp.task_id)

    archive_dir = repo_root / "orga" / "tasks" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    archived_folder = archive_dir / active_folder.name
    if archived_folder.exists():
        raise FileExistsError(f"Archive folder already exists: {archived_folder}")

    shutil.move(str(active_folder), str(archived_folder))

    archived_rel = f"orga/tasks/archive/{archived_folder.name}/"
    tasks_md = repo_root / "orga" / "tasks" / "TASKS.md"
    update_tasks_index(tasks_md, inp.task_id, archived_rel, inp.force)

    branch = f"chore/finish-{inp.task_id.lower()}"
    pr_title = f"Finish {inp.task_id}"
    commit_message = f"Finish {inp.task_id}"

    write_github_output(branch=branch, pr_title=pr_title, commit_message=commit_message, archived_folder=archived_rel)


if __name__ == "__main__":
    main()
