"""Infrastructure adapters for Self Rewrite context."""

import json
import os
import subprocess
import urllib.request
from pathlib import Path

from packages.self_rewrite.domain.models import Patch, SelfRewriteJob
from packages.self_rewrite.domain.ports import (
    GitPullRequestPublisherPort,
    SelfRewriteRepository,
)


class InMemorySelfRewriteRepository(SelfRewriteRepository):
    def __init__(self) -> None:
        self._store: dict[str, SelfRewriteJob] = {}

    def save(self, job: SelfRewriteJob) -> SelfRewriteJob:
        self._store[job.id] = job
        return job

    def find_by_id(self, job_id: str) -> SelfRewriteJob | None:
        return self._store.get(job_id)

    def list_all(self) -> list[SelfRewriteJob]:
        return list(self._store.values())


class PhysicalGitAutoPRAdapter(GitPullRequestPublisherPort):
    """Applies patch via Git CLI and opens GitHub Pull Request via REST API."""

    def __init__(
        self,
        repo_root: Path,
        github_repo: str = "eaos/eaos",
        github_token: str | None = None,
    ) -> None:
        self.repo_root = repo_root
        self.github_repo = github_repo
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")

    def publish_pull_request(
        self,
        job_id: str,
        patch: Patch,
        pr_title: str,
        pr_description: str,
    ) -> dict[str, str | bool]:
        branch_name = f"feature/auto-fix-{job_id.lower()}"

        try:
            # 1. Create temporary patch file
            patch_file = self.repo_root / f".patch_{job_id}.diff"
            patch_file.write_text(patch.diff_content, encoding="utf-8")

            # 2. Execute Local Git CLI commands
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "apply", str(patch_file)],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-am", f"fix(auto): {pr_title}"],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
            )

            # Cleanup patch file
            if patch_file.exists():
                patch_file.unlink()

            # 3. Create GitHub Pull Request via REST API if token exists
            pr_url = f"https://github.com/{self.github_repo}/tree/{branch_name}"
            pr_created = False

            if self.github_token:
                pr_created = self._create_github_pr(
                    branch_name=branch_name,
                    title=pr_title,
                    body=pr_description,
                )

            return {
                "success": True,
                "branch": branch_name,
                "pr_url": pr_url,
                "github_pr_created": pr_created,
            }

        except Exception as err:
            return {
                "success": False,
                "error": str(err),
                "branch": branch_name,
            }

    def _create_github_pr(
        self, branch_name: str, title: str, body: str
    ) -> bool:
        """Sends HTTP POST request to GitHub API v3 /repos/{owner}/{repo}/pulls."""
        url = f"https://api.github.com/repos/{self.github_repo}/pulls"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }
        data = {
            "title": title,
            "body": body,
            "head": branch_name,
            "base": "main",
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req) as resp:
                return bool(getattr(resp, 'status', None) == 201)
        except Exception:
            return False
