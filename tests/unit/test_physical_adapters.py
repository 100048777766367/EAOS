"""Unit tests for Physical Auto-PR and OPA Adapters."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from packages.policy_engine.infrastructure.adapters import OPARegoPolicyAdapter
from packages.self_rewrite.domain.models import Patch
from packages.self_rewrite.infrastructure.adapters import (
    PhysicalGitAutoPRAdapter,
)


def test_physical_git_auto_pr_adapter_local_flow(tmp_path: Path) -> None:
    patch_obj = Patch(
        file_path="packages/test.py",
        diff_content="--- a/test.py\n+++ b/test.py\n@@ -1 +1 @@\n-a = 1\n+a = 2\n",
    )

    adapter = PhysicalGitAutoPRAdapter(repo_root=tmp_path)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        result = adapter.publish_pull_request(
            job_id="JOB-101",
            patch=patch_obj,
            pr_title="Fix Database Connection",
            pr_description="Auto patch created by AI Agent",
        )

        assert result["success"] is True
        assert result["branch"] == "feature/auto-fix-job-101"


def test_opa_rego_policy_adapter_mock_response() -> None:
    adapter = OPARegoPolicyAdapter(opa_host="http://localhost:8181")

    mock_opa_json = json.dumps(
        {
            "result": {
                "allow": False,
                "violations": [
                    "Forbidden infrastructure import in domain layer."
                ],
            }
        }
    ).encode("utf-8")

    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.read.return_value = mock_opa_json
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        allow, violations = adapter.evaluate_opa_rego(
            policy_path="eaos/architecture/imports",
            input_context={
                "imported_module": "sqlalchemy",
                "layer": "domain",
            },
        )

        assert allow is False
        assert len(violations) == 1
        assert "Forbidden infrastructure import" in violations[0]
