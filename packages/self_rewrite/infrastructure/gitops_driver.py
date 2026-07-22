import base64
import json
import logging
import os
import urllib.request
import uuid

from pydantic import BaseModel

logger = logging.getLogger("eaos.gitops")


class GitHubPRResponse(BaseModel):
    """Phản hồi kết quả tạo Pull Request từ GitHub API Driver."""

    status: str
    pr_number: int
    pr_url: str
    branch_name: str
    commit_sha: str


class GitHubGitOpsDriver:
    """Driver tương tác trực tiếp với GitHub REST API để thực thi GitOps."""

    def __init__(

        self,
        owner: str = "100048777766367",
        repo: str = "EAOS",
        token: str | None = None,
    ) -> None:
        self.owner = owner
        self.repo = repo
        self.token = token or os.getenv("GITHUB_TOKEN", "")

    def create_pull_request(
        self,
        branch_name: str,
        file_path: str,
        content: str,
        commit_message: str,
        pr_title: str,
    ) -> GitHubPRResponse:
        """Tạo branch mới, commit tệp tin và mở Pull Request thật trên GitHub."""
        if self.token:
            try:
                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "EAOS-Autonomous-Engine",
                }

                ref_url = (
                    f"https://api.github.com/repos/{self.owner}/{self.repo}"
                    "/git/ref/heads/main"
                )
                ref_req = urllib.request.Request(ref_url, headers=headers)
                with urllib.request.urlopen(ref_req) as resp:
                    main_data = json.loads(resp.read().decode("utf-8"))
                    main_sha = main_data["object"]["sha"]

                branch_url = (
                    f"https://api.github.com/repos/{self.owner}/{self.repo}"
                    "/git/refs"
                )
                branch_payload = json.dumps(
                    {"ref": f"refs/heads/{branch_name}", "sha": main_sha}
                ).encode("utf-8")
                b_req = urllib.request.Request(
                    branch_url, data=branch_payload, headers=headers
                )
                urllib.request.urlopen(b_req)

                file_url = (
                    f"https://api.github.com/repos/{self.owner}/{self.repo}"
                    f"/contents/{file_path}"
                )
                file_payload = json.dumps(
                    {
                        "message": commit_message,
                        "content": base64.b64encode(content.encode()).decode(),
                        "branch": branch_name,
                    }
                ).encode("utf-8")
                f_req = urllib.request.Request(
                    file_url,
                    data=file_payload,
                    headers=headers,
                    method="PUT",
                )
                with urllib.request.urlopen(f_req) as f_resp:
                    f_data = json.loads(f_resp.read().decode("utf-8"))
                    commit_sha = f_data["commit"]["sha"]

                pr_url = (
                    f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls"
                )
                pr_payload = json.dumps(
                    {
                        "title": pr_title,
                        "head": branch_name,
                        "base": "main",
                        "body": "Tự động sinh bởi EAOS Self-Rewrite Engine.",
                    }
                ).encode("utf-8")
                pr_req = urllib.request.Request(
                    pr_url, data=pr_payload, headers=headers
                )
                with urllib.request.urlopen(pr_req) as pr_resp:
                    pr_data = json.loads(pr_resp.read().decode("utf-8"))
                    return GitHubPRResponse(
                        status="SUCCESS",
                        pr_number=pr_data["number"],
                        pr_url=pr_data["html_url"],
                        branch_name=branch_name,
                        commit_sha=commit_sha,
                    )
            except Exception as err:
                logger.warning("GitHub API Call failed, falling back: %s", err)

        fake_sha = uuid.uuid4().hex[:7]
        fake_pr_num = 100 + len(branch_name) % 50
        return GitHubPRResponse(
            status="SIMULATED_GITOPS",
            pr_number=fake_pr_num,
            pr_url=(
                f"https://github.com/{self.owner}/{self.repo}"
                f"/pull/{fake_pr_num}"
            ),
            branch_name=branch_name,
            commit_sha=fake_sha,
        )