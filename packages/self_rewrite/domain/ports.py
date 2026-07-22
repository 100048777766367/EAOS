"""Domain ports for Self Rewrite context."""

from typing import Protocol

from packages.self_rewrite.domain.models import Patch, SelfRewriteJob


class SelfRewriteRepository(Protocol):
    def save(self, job: SelfRewriteJob) -> SelfRewriteJob: ...

    def find_by_id(self, job_id: str) -> SelfRewriteJob | None: ...

    def list_all(self) -> list[SelfRewriteJob]: ...


class GitPullRequestPublisherPort(Protocol):
    """Port for applying physical patches and publishing Pull Requests to GitHub."""

    def publish_pull_request(
        self,
        job_id: str,
        patch: Patch,
        pr_title: str,
        pr_description: str,
    ) -> dict[str, str | bool]: ...
