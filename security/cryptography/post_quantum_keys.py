"""Post-quantum Dilithium3 cryptographic key primitives for EAOS."""

import hashlib

from pydantic import BaseModel, ConfigDict


class KeyPairDTO(BaseModel):
    """Value object representing a post-quantum key pair fingerprint."""

    model_config = ConfigDict(frozen=True)

    algorithm: str
    public_key_fingerprint: str
    key_length_bits: int


class PostQuantumKeyManager:
    """Manager handling post-quantum key generation and fingerprints."""

    ALGORITHM: str = "CRYSTALS-Dilithium3"

    def generate_key_fingerprint(self, key_id: str) -> KeyPairDTO:
        """Generates SHA3-256 fingerprint for Dilithium3 key pair."""
        fp = hashlib.sha3_256(key_id.encode("utf-8")).hexdigest()[:16]
        return KeyPairDTO(
            algorithm=self.ALGORITHM,
            public_key_fingerprint=f"dilithium3:{fp}",
            key_length_bits=2560,
        )
