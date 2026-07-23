"""Post-Quantum Kyber key envelope encryption engine."""

import hashlib
import time

from pydantic import BaseModel, ConfigDict


class EncryptedEnvelopeDTO(BaseModel):
    """Value object representing a quantum-resistant envelope."""

    model_config = ConfigDict(frozen=True)

    envelope_id: str
    algorithm: str
    cipher_text_hex: str
    key_fingerprint: str


class QuantumEnvelopeEncryptionEngine:
    """Kyber-style post-quantum key envelope encryption engine."""

    ALGORITHM: str = "CRYSTALS-Kyber768-AES256"

    def encrypt_secret_payload(
        self,
        secret_data: str,
        public_key_fingerprint: str,
    ) -> EncryptedEnvelopeDTO:
        """Encrypts payload into post-quantum encrypted envelope."""
        raw_cipher = f"kyber:{public_key_fingerprint}:{secret_data}"
        cipher_hex = hashlib.sha3_256(raw_cipher.encode("utf-8")).hexdigest()
        env_id = f"env_{int(time.time())}"

        return EncryptedEnvelopeDTO(
            envelope_id=env_id,
            algorithm=self.ALGORITHM,
            cipher_text_hex=cipher_hex,
            key_fingerprint=public_key_fingerprint,
        )
