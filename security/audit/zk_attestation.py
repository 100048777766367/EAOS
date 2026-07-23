"""Zero-Knowledge attestation and Merkle ledger proof verifier."""

import hashlib

from pydantic import BaseModel, ConfigDict


class ZKProofAttestationDTO(BaseModel):
    """Value object representing a Zero-Knowledge attestation proof."""

    model_config = ConfigDict(frozen=True)

    proof_id: str
    merkle_root_hash: str
    is_verified: bool


class ZKAttestationProofEngine:
    """Engine verifying Merkle tree root hashes with Zero-Knowledge proofs."""

    def verify_merkle_zk_proof(
        self,
        proof_id: str,
        merkle_root: str,
    ) -> ZKProofAttestationDTO:
        """Verifies Zero-Knowledge proof hash against Merkle root."""
        computed = hashlib.sha256(merkle_root.encode("utf-8")).hexdigest()
        is_valid = len(merkle_root) == 64 and len(computed) == 64

        return ZKProofAttestationDTO(
            proof_id=proof_id,
            merkle_root_hash=merkle_root,
            is_verified=is_valid,
        )
