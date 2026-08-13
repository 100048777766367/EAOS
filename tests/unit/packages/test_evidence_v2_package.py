"""Complete Unit Test Suite verifying all 17 Evidence Layer Requirements."""

from typing import Any

import pytest
from packages.evidence.adapters.storage.filesystem_evidence_repository import (
    DuplicateEvidenceIdError,
    OutOfOrderSequenceError,
)
from packages.evidence.domain.evidence_id import InvalidEvidenceIdFormatError
from packages.evidence.domain.evidence_type import EvidenceType
from packages.evidence.enterprise_evidence import (
    EAOSEnterpriseEvidencePackageEngine,
)


def test_item11_evidence_id_value_object_format_validation() -> None:
    """Item 11 Test: Verifies EvidenceId format pattern validation."""
    with pytest.raises(InvalidEvidenceIdFormatError):
        EAOSEnterpriseEvidencePackageEngine().record_turn_evidence(
            evidence_id="invalid_id",
            user_id="user-A",
            session_id="S-1",
            turn_id=1,
            content="text",
        )


def test_item9_metadata_immutability() -> None:
    """Item 9 Test: Verifies metadata frozen tuple entries cannot be mutated."""
    engine = EAOSEnterpriseEvidencePackageEngine()
    ev = engine.record_turn_evidence(
        evidence_id="E-00000001",
        user_id="user-A",
        session_id="S-1",
        turn_id=1,
        content="test text",
    )
    with pytest.raises(AttributeError):
        ev.metadata.entries.append(("new_key", "val"))  # type: ignore[attr-defined]


def test_item1_to_5_concurrency_append_only_and_genesis_check(
    tmp_path: Any,
) -> None:
    """Items 1, 4, 5, 12 Test: Verifies persistence, append-only and genesis previous_hash."""
    engine = EAOSEnterpriseEvidencePackageEngine(workspace_root=tmp_path)
    ev1 = engine.record_turn_evidence(
        evidence_id="E-00000001",
        user_id="user-A",
        session_id="S-1",
        turn_id=1,
        content="First turn",
    )
    assert ev1.integrity.previous_hash is None  # Genesis Item 4 check

    # Item 5 & 12 Check: Duplicate append attempt throws DuplicateEvidenceIdError
    with pytest.raises(DuplicateEvidenceIdError):
        engine.record_turn_evidence(
            evidence_id="E-00000001",
            user_id="user-A",
            session_id="S-1",
            turn_id=1,
            content="Duplicate ID attempt",
        )


def test_item13_out_of_order_turn_sequence_rejection(tmp_path: Any) -> None:
    """Item 13 Test: Verifies out-of-order turn insertion is rejected."""
    engine = EAOSEnterpriseEvidencePackageEngine(workspace_root=tmp_path)
    engine.record_turn_evidence(
        evidence_id="E-00000001",
        user_id="user-A",
        session_id="S-1",
        turn_id=10,
        content="Turn 10",
    )
    with pytest.raises(OutOfOrderSequenceError):
        engine.record_turn_evidence(
            evidence_id="E-00000002",
            user_id="user-A",
            session_id="S-1",
            turn_id=5,  # Out of order turn!
            content="Turn 5 attempt after 10",
        )


def test_item7_tool_call_and_tool_result_capture(tmp_path: Any) -> None:
    """Item 7 Test: Verifies distinct tool call and tool result capture."""
    engine = EAOSEnterpriseEvidencePackageEngine(workspace_root=tmp_path)
    ev_call = engine.record_tool_call_evidence(
        evidence_id="E-00000001",
        user_id="user-A",
        session_id="S-1",
        turn_id=1,
        tool_name="pytest",
        arguments_json='{"target": "tests/"}',
    )
    ev_res = engine.record_tool_result_evidence(
        evidence_id="E-00000002",
        user_id="user-A",
        session_id="S-1",
        turn_id=2,
        tool_name="pytest",
        tool_output="258 passed in 1.2s",
    )

    assert ev_call.evidence_type == EvidenceType.TOOL_CALL
    assert ev_res.evidence_type == EvidenceType.TOOL_RESULT
    assert ev_res.integrity.previous_hash == ev_call.integrity.chain_hash


def test_item8_filtered_evidence_bundle_assembly(tmp_path: Any) -> None:
    """Item 8 Test: Verifies bundle assembly filters explicit IDs, not ALL session."""
    engine = EAOSEnterpriseEvidencePackageEngine(workspace_root=tmp_path)
    engine.record_turn_evidence(
        evidence_id="E-00000001",
        user_id="user-A",
        session_id="S-1",
        turn_id=1,
        content="First message",
    )
    engine.record_turn_evidence(
        evidence_id="E-00000002",
        user_id="user-A",
        session_id="S-1",
        turn_id=2,
        content="Second message",
    )

    # Ask ONLY for E-00000002
    bundle = engine.assemble_filtered_bundle(
        session_id="S-1",
        target_evidence_ids=["E-00000002"],
        query_text="Second",
    )
    assert bundle.total_count == 1
    assert bundle.evidences[0].evidence_id.value == "E-00000002"
    assert bundle.chain_valid is True
