import json
import logging
import urllib.request
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger("eaos.opa")


class OPAPolicyResult(BaseModel):
    """Kết quả thẩm định chính sách động từ Open Policy Agent."""

    allow: bool = Field(..., description="Trạng thái cho phép")
    violations: list[str] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)


class OPAEngineAdapter:
    """Adapter kết nối Open Policy Agent (OPA) Server qua REST API."""

    def __init__(
        self,
        opa_url: str = "http://localhost:8181/v1/data/eaos/authz",
        timeout_seconds: float = 2.0,
    ) -> None:
        self.opa_url = opa_url
        self.timeout_seconds = timeout_seconds

    def evaluate_policy(self, input_data: dict[str, Any]) -> OPAPolicyResult:
        """Gửi payload sang OPA Server hoặc fallback xử lý nội bộ nếu OPA offline."""
        try:
            req_body = json.dumps({"input": input_data}).encode("utf-8")
            req = urllib.request.Request(
                self.opa_url,
                data=req_body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                result = res_json.get("result", {})
                allow = result.get("allow", True)
                violations = result.get("violations", [])
                return OPAPolicyResult(
                    allow=allow,
                    violations=violations,
                    metrics={"engine": "OPA_HTTP", "status": "ONLINE"},
                )
        except Exception as err:
            logger.warning("OPA Server offline, using local fallback: %s", err)
            version = input_data.get("__version", 1)
            allow = isinstance(version, int) and version >= 1
            violations = [] if allow else ["Invalid __version format"]
            return OPAPolicyResult(
                allow=allow,
                violations=violations,
                metrics={"engine": "LOCAL_FALLBACK", "status": "OFFLINE"},
            )
