"""Zero-Trust Vault ephemeral secret token generator for EAOS."""

import time

from pydantic import BaseModel, ConfigDict


class EphemeralVaultToken(BaseModel):
    """Value object representing an ephemeral Vault secret token."""

    model_config = ConfigDict(frozen=True)

    token_id: str
    secret_path: str
    lease_duration_sec: int
    status: str


class VaultEphemeralSigner:
    """Signer issuing dynamic time-bound access tokens for secrets."""

    def generate_ephemeral_token(
        self,
        secret_path: str,
        ttl_sec: int = 3600,
    ) -> EphemeralVaultToken:
        """Generates time-limited dynamic lease token for secret path."""
        token_id = f"vtok_{int(time.time())}"
        return EphemeralVaultToken(
            token_id=token_id,
            secret_path=secret_path,
            lease_duration_sec=ttl_sec,
            status="ACTIVE",
        )
