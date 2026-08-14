from dxs.evidence.ledger import EvidenceLedger
from dxs.evidence.timeline import EvidenceTimeline


def test_evidence_ledger(tmp_path):
    ledger = EvidenceLedger(tmp_path)

    file = ledger.record(
        "diagnose",
        {"status": "PASS"},
    )

    assert file.exists()

    timeline = EvidenceTimeline(tmp_path)

    events = timeline.list_events()

    assert len(events) == 1
    assert events[0]["hash"]
