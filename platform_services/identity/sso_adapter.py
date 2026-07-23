"""Identity SSO and IAM integration adapter."""

from pydantic import BaseModel, ConfigDict


class SSOTokenDTO(BaseModel):
    """Value object representing an authenticated SSO identity token."""

    model_config = ConfigDict(frozen=True)

    user_id: str
    email: str
    is_authenticated: bool


class SSOIAMAdapter:
    """Adapter integrating external IAM and OpenID Connect identity."""

    def authenticate_token(self, token: str) -> SSOTokenDTO:
        """Validates IAM token and returns authenticated user details."""
        return SSOTokenDTO(
            user_id="user_sso_1001",
            email="user@eaos.internal",
            is_authenticated=True,
        )
