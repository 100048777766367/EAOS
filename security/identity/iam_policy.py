"""Identity, IAM policies, and RBAC/ABAC access control models for EAOS."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class IAMRolePolicyDTO(BaseModel):
    """Value object representing an IAM role permission policy."""

    model_config = ConfigDict(frozen=True)

    role_name: str
    allowed_actions: list[str]
    is_admin: bool


class IAMPolicyEngine:
    """Engine evaluating RBAC/ABAC access control permissions."""

    ROLE_PERMISSIONS: ClassVar[dict[str, list[str]]] = {
        "ADMIN": ["READ", "WRITE", "DELETE", "AMEND_CONSTITUTION"],
        "ARCHITECT": ["READ", "WRITE", "COMPILE_POLICY"],
        "OPERATOR": ["READ", "TRIGGER_BUILD"],
        "VIEWER": ["READ"],
    }

    def evaluate_access_permission(
        self,
        user_role: str,
        requested_action: str,
    ) -> bool:
        """Evaluates whether role has permission for requested action."""
        allowed = self.ROLE_PERMISSIONS.get(user_role.upper(), [])
        return requested_action.upper() in allowed or "AMEND_CONSTITUTION" in allowed
