from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.agent.domain.git_models import GitOperationResult

"""Git Agent Port Protocol."""


@runtime_checkable
class GitAgentPort(Protocol):
    """Port protocol for Level 10 Git Agent automation."""

    async def create_feature_branch(self, branch_name: str) -> GitOperationResult: ...

    async def auto_commit_and_pr(self, message: str, feature_id: str) -> GitOperationResult: ...
