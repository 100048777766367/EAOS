"""External Repository Manager Adapter."""

from __future__ import annotations

import subprocess
from pathlib import Path

from packages.federation.domain.repository_onboarding_models import (
    ExternalRepositoryDTO,
    OnboardingReportDTO,
    StackType,
)
from packages.federation.ports.repository_onboarding_port import (
    RepositoryOnboardingPort,
)


class ExternalRepositoryManagerAdapter(RepositoryOnboardingPort):
    """Adapter cloning, inspecting, and installing external repos."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.external_dir = self.root / "runtime" / "external_repos"
        self._installed: dict[str, ExternalRepositoryDTO] = {}

    async def install_repository(self, repo_slug_or_url: str) -> OnboardingReportDTO:
        repo_name = repo_slug_or_url.split("/")[-1].replace(".git", "")
        target_path = self.external_dir / repo_name
        self.external_dir.mkdir(parents=True, exist_ok=True)

        log_lines: list[str] = []

        if not target_path.exists():
            git_url = (
                repo_slug_or_url
                if repo_slug_or_url.startswith("http")
                else f"https://github.com/{repo_slug_or_url}.git"
            )
            res = self._run_cmd(["git", "clone", git_url, str(target_path)])
            log_lines.append(f"Git Clone: {res}")
        else:
            log_lines.append(f"Repository '{repo_name}' already exists.")

        stack = self._detect_stack(target_path)
        log_lines.append(f"Detected Stack: {stack}")

        if stack == StackType.PYTHON and (
            (target_path / "pyproject.toml").exists() or (target_path / "setup.py").exists()
        ):
            res = self._run_cmd(["uv", "pip", "install", "-e", str(target_path)])
            log_lines.append(f"UV Pip Install: {res[:200]}")

        repo_dto = ExternalRepositoryDTO(
            repo_name=repo_name,
            repo_url=repo_slug_or_url,
            stack_type=stack,
            installed_path=str(target_path),
            is_active=True,
        )
        self._installed[repo_name] = repo_dto

        return OnboardingReportDTO(
            success=True,
            repo_name=repo_name,
            stack_type=stack,
            capability_id=f"cap-external-{repo_name}",
            installation_log="\n".join(log_lines),
        )

    def list_installed_repositories(self) -> list[ExternalRepositoryDTO]:
        return list(self._installed.values())

    def _detect_stack(self, repo_path: Path) -> StackType:
        if (repo_path / "pyproject.toml").exists() or (repo_path / "requirements.txt").exists():
            return StackType.PYTHON
        if (repo_path / "package.json").exists():
            return StackType.NODEJS
        if (repo_path / "docker-compose.yml").exists() or (repo_path / "Dockerfile").exists():
            return StackType.DOCKER
        return StackType.UNKNOWN

    def _run_cmd(self, cmd: list[str]) -> str:
        try:
            res = subprocess.run(
                cmd,
                cwd=str(self.root),
                capture_output=True,
                text=True,
                timeout=60,
            )
            return res.stdout or res.stderr
        except Exception as err:
            return f"Execution error: {err}"
