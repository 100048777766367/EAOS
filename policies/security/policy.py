"""Security Policy-as-Code domain specification for EAOS."""

from pydantic import BaseModel, ConfigDict


class SecurityPolicyDTO(BaseModel):
    """Value object representing an active security policy rule."""

    model_config = ConfigDict(frozen=True)

    policy_id: str
    rule_name: str
    enforced: bool


class SecurityPolicyEngine:
    """Policy engine enforcing Zero-Trust security rules."""

    def get_active_policies(self) -> list[SecurityPolicyDTO]:
        """Returns active security policies."""
        return [
            SecurityPolicyDTO(
                policy_id="POL-SEC-01",
                rule_name="Post-Quantum Dilithium3 Attestation Required",
                enforced=True,
            )
        ]
