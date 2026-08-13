from __future__ import annotations

import subprocess
from pathlib import Path

from packages.agent.domain.git_models import GitOperationResult
from packages.agent.ports.git_port import GitAgentPort

"""Level 10 Git Agent Adapter."""


class GitAgentAdapter(GitAgentPort):
    """Adapter automating Git branch, commit, and PR creation."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    async def create_feature_branch(self, branch_name: str) -> GitOperationResult:
        clean_branch = f"feature/{branch_name.replace(' ', '-').lower()}"
        res = self._run_git(["checkout", "-b", clean_branch])
        if res.returncode == 0 or "already exists" in res.stderr:
            return GitOperationResult(
                success=True,
                branch_name=clean_branch,
                commit_message="Created feature branch",
            )
        return GitOperationResult(
            success=False,
            branch_name=clean_branch,
            error=res.stderr or res.stdout,
        )

    async def auto_commit_and_pr(self, message: str, feature_id: str) -> GitOperationResult:
        commit_msg = f"feat({feature_id}): {message}"

        self._run_git(["add", "."])
        res = self._run_git(["commit", "-m", commit_msg])

        if res.returncode != 0 and "nothing to commit" not in res.stdout:
            return GitOperationResult(success=False, error=res.stderr or res.stdout)

        hash_res = self._run_git(["rev-parse", "--short", "HEAD"])
        c_hash = hash_res.stdout.strip() if hash_res.returncode == 0 else "head"
        pr_url = f"https://github.com/eaos/eaos/pull/new/{feature_id}"

        return GitOperationResult(
            success=True,
            branch_name="current",
            commit_hash=c_hash,
            commit_message=commit_msg,
            pr_url=pr_url,
        )

    def _run_git(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=str(self.root),
            capture_output=True,
            text=True,
            timeout=30,
        )
