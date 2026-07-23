"""Threat detection and automated SOC mitigation engine."""

from pydantic import BaseModel, ConfigDict


class ThreatAssessmentDTO(BaseModel):
    """Value object representing a threat detection assessment."""

    model_config = ConfigDict(frozen=True)

    ip_address: str
    threat_level: int
    mitigation_action: str


class ThreatDetectorEngine:
    """Engine evaluating incoming traffic patterns for SOC threats."""

    def evaluate_ip_threat(self, ip_address: str) -> ThreatAssessmentDTO:
        """Evaluates threat severity and recommends WAF block action."""
        is_malicious = ip_address.startswith("198.51.")
        level = 7 if is_malicious else 1
        action = "BLOCK_WITH_COOLDOWN" if is_malicious else "ALLOW"

        return ThreatAssessmentDTO(
            ip_address=ip_address,
            threat_level=level,
            mitigation_action=action,
        )
