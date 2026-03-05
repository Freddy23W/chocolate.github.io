from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Repo:
    owner: str
    name: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_repo_from_remote_url(url: str) -> Repo:
    url = url.strip()

    m = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$", url)
    if not m:
        raise ValueError(f"Could not parse GitHub repo from remote URL: {url!r}")

    return Repo(owner=m.group("owner"), name=m.group("repo"))


def _infer_repo_from_git_config(repo_root: Path) -> Repo:
    config_path = repo_root / ".git" / "config"
    if not config_path.exists():
        raise FileNotFoundError("Missing .git/config. Cannot infer owner/repo.")

    raw = _read_text(config_path)

    # naive parse: find first origin url
    # [remote "origin"]\n\turl = ...
    m = re.search(r"\[remote \"origin\"\](?:\r?\n|.)*?\r?\n\s*url\s*=\s*(?P<url>.+)", raw)
    if not m:
        raise ValueError("Could not find remote 'origin' url in .git/config")

    return _parse_repo_from_remote_url(m.group("url"))


def _load_repo(repo_root: Path) -> Repo:
    repo_s = (os.environ.get("GH_REPO") or "").strip()
    if repo_s:
        if "/" not in repo_s:
            raise ValueError("GH_REPO must look like 'owner/repo'")
        owner, name = repo_s.split("/", 1)
        return Repo(owner=owner, name=name)

    return _infer_repo_from_git_config(repo_root)


def _load_token() -> str:
    for name in ("GH_TOKEN", "GH_PR_TOKEN", "GITHUB_TOKEN"):
        val = os.environ.get(name)
        if val and val.strip():
            return val.strip()
    raise ValueError("Missing token. Set GH_TOKEN (recommended) or GH_PR_TOKEN.")


def _parse_inputs(kv_list: list[str]) -> dict[str, str]:
    inputs: dict[str, str] = {}
    for kv in kv_list:
        if "=" not in kv:
            raise ValueError(f"Invalid --input {kv!r}. Use key=value")
        k, v = kv.split("=", 1)
        k = k.strip()
        if not k:
            raise ValueError(f"Invalid --input {kv!r}. Empty key")
        inputs[k] = v
    return inputs


def dispatch_workflow(*, api_url: str, repo: Repo, workflow: str, ref: str, inputs: dict[str, str], token: str) -> None:
    workflow = workflow.strip()
    if not workflow:
        raise ValueError("workflow must be non-empty")

    url = f"{api_url.rstrip('/')}/repos/{repo.owner}/{repo.name}/actions/workflows/{workflow}/dispatches"
    payload: dict[str, Any] = {"ref": ref}
    if inputs:
        payload["inputs"] = inputs

    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "template-dispatch-workflow",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=30) as resp:
            # success is 204 with empty body
            if resp.status not in (200, 201, 202, 204):
                raise RuntimeError(f"Unexpected response status: {resp.status}")
    except HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        raise RuntimeError(f"GitHub API error: HTTP {e.code} {e.reason}. {body}") from e
    except URLError as e:
        raise RuntimeError(f"Network error calling GitHub API: {e}") from e


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Dispatch a GitHub Actions workflow_dispatch run via GitHub API")
    parser.add_argument("--workflow", required=True, help="Workflow file name, e.g. start-task.yml")
    parser.add_argument("--ref", default=os.environ.get("GH_REF") or "main", help="Git ref (default: GH_REF or main)")
    parser.add_argument("--input", action="append", default=[], help="Workflow input key=value (repeatable)")
    parser.add_argument(
        "--api-url",
        default=os.environ.get("GH_API_URL") or "https://api.github.com",
        help="GitHub API base URL (default: GH_API_URL or https://api.github.com)",
    )

    args = parser.parse_args(argv)

    repo_root = _repo_root()
    repo = _load_repo(repo_root)
    token = _load_token()
    inputs = _parse_inputs(args.input)

    dispatch_workflow(api_url=args.api_url, repo=repo, workflow=args.workflow, ref=args.ref, inputs=inputs, token=token)

    print("Dispatched workflow.")
    print(f"- Repo: {repo.owner}/{repo.name}")
    print(f"- Workflow: {args.workflow}")
    print(f"- Ref: {args.ref}")
    if inputs:
        print(f"- Inputs: {', '.join(f'{k}={v}' for k, v in inputs.items())}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
