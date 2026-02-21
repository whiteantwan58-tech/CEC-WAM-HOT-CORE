#!/usr/bin/env python3
"""Audit GitHub repositories for 5D interface deployment readiness."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


API = "https://api.github.com"


@dataclass
class RepoStatus:
    name: str
    private: bool
    default_branch: str
    archived: bool
    push_permission: str
    has_streamlit: bool
    has_static: bool
    pages_status: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "private": self.private,
            "default_branch": self.default_branch,
            "archived": self.archived,
            "push_permission": self.push_permission,
            "has_streamlit": self.has_streamlit,
            "has_static": self.has_static,
            "pages_status": self.pages_status,
        }


class GitHubClient:
    def __init__(self, token: str | None = None) -> None:
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/vnd.github+json"})
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> requests.Response:
        resp = self.session.get(f"{API}{path}", params=params, timeout=20)
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            raise RuntimeError("GitHub API rate limit exceeded. Set GITHUB_TOKEN and retry.")
        return resp

    def list_repos(self, owner: str) -> list[dict[str, Any]]:
        repos: list[dict[str, Any]] = []
        page = 1
        while True:
            resp = self.get(
                f"/users/{owner}/repos",
                params={"per_page": 100, "page": page, "type": "owner", "sort": "updated"},
            )
            if resp.status_code == 404:
                raise RuntimeError(f"Owner '{owner}' not found.")
            resp.raise_for_status()
            batch = resp.json()
            if not batch:
                break
            repos.extend(batch)
            page += 1
        return repos

    def has_file(self, owner: str, repo: str, branch: str, path: str) -> bool:
        resp = self.get(f"/repos/{owner}/{repo}/contents/{path}", params={"ref": branch})
        return resp.status_code == 200

    def pages_status(self, owner: str, repo: str) -> str:
        resp = self.get(f"/repos/{owner}/{repo}/pages")
        if resp.status_code == 404:
            return "disabled"
        if not resp.ok:
            return f"error:{resp.status_code}"
        data = resp.json()
        return data.get("status") or "configured"


def permission_label(repo_json: dict[str, Any]) -> str:
    permissions = repo_json.get("permissions") or {}
    if permissions.get("admin"):
        return "admin"
    if permissions.get("push"):
        return "write"
    if permissions.get("pull"):
        return "read"
    return "unknown"


def audit_owner(owner: str, client: GitHubClient) -> list[RepoStatus]:
    statuses: list[RepoStatus] = []
    repos = client.list_repos(owner)
    for repo in repos:
        name = repo["name"]
        default_branch = repo.get("default_branch", "main")
        has_streamlit = any(
            client.has_file(owner, name, default_branch, entry)
            for entry in ("streamlit_app.py", "app.py")
        )
        has_static = any(
            client.has_file(owner, name, default_branch, entry)
            for entry in ("index.html", "dashboard.html")
        )
        pages = client.pages_status(owner, name)
        statuses.append(
            RepoStatus(
                name=name,
                private=repo.get("private", False),
                default_branch=default_branch,
                archived=repo.get("archived", False),
                push_permission=permission_label(repo),
                has_streamlit=has_streamlit,
                has_static=has_static,
                pages_status=pages,
            )
        )
    return statuses


def print_table(statuses: list[RepoStatus]) -> None:
    header = "repo | permission | streamlit | static | github_pages | archived"
    print(header)
    print("-" * len(header))
    for item in statuses:
        print(
            f"{item.name} | {item.push_permission} | "
            f"{'yes' if item.has_streamlit else 'no'} | "
            f"{'yes' if item.has_static else 'no'} | {item.pages_status} | "
            f"{'yes' if item.archived else 'no'}"
        )


def write_report(path: Path, owner: str, statuses: list[RepoStatus]) -> None:
    payload = {
        "owner": owner,
        "repo_count": len(statuses),
        "repos": [s.as_dict() for s in statuses],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check all repositories under an owner for 5D interface deployment readiness."
    )
    parser.add_argument("--owner", default="whiteantwan58-tech", help="GitHub owner/org name")
    parser.add_argument(
        "--report",
        default="reports/repo_interface_audit.json",
        help="Path for JSON report output",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    client = GitHubClient(token=token)

    try:
        statuses = audit_owner(args.owner, client)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print_table(statuses)
    write_report(Path(args.report), args.owner, statuses)
    print(f"\nReport written to {args.report}")

    missing_write = [s.name for s in statuses if s.push_permission in {"read", "unknown"}]
    if missing_write:
        print("\nRepositories with non-write access (likely deploy-key/read-only issue):")
        for name in missing_write:
            print(f"- {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
