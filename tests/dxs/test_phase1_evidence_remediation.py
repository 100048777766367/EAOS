from dxs.evidence import EvidenceService, EvidenceStatus
from dxs.remediation import RemediationService, RemediationStatus


def test_evidence_lifecycle() -> None:
    service = EvidenceService()

    evidence = service.capture(
        "architecture",
        "valid",
        "test",
    )

    assert evidence.status is EvidenceStatus.OPEN
    assert service.verify(evidence).status is EvidenceStatus.VERIFIED
    assert service.supersede(evidence).status is EvidenceStatus.SUPERSEDED


def test_remediation_lifecycle() -> None:
    service = RemediationService()

    remediation = service.create(
        "fix",
        "Resolve diagnostic finding.",
    )

    assert remediation.status is RemediationStatus.OPEN
    assert service.resolve(remediation).status is RemediationStatus.RESOLVED
    assert service.block(remediation).status is RemediationStatus.BLOCKED
