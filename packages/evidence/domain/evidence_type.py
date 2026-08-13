from __future__ import annotations

from enum import StrEnum

"""Domain Enum for Categorized Evidence Types across Agent Lifecycle."""


class EvidenceType(StrEnum):
    """Categorized evidence types for complete operational fact tracking."""

    CONVERSATION_TURN = "CONVERSATION_TURN"
    USER_MESSAGE = "USER_MESSAGE"
    ASSISTANT_MESSAGE = "ASSISTANT_MESSAGE"
    TOOL_CALL = "TOOL_CALL"
    TOOL_RESULT = "TOOL_RESULT"
    CODE_CHANGE = "CODE_CHANGE"
    FILE_SNAPSHOT = "FILE_SNAPSHOT"
    TEST_RESULT = "TEST_RESULT"
    VERIFICATION_RESULT = "VERIFICATION_RESULT"
    SYSTEM_EVENT = "SYSTEM_EVENT"
    POLICY_DECISION = "POLICY_DECISION"
    ACTION_DECISION = "ACTION_DECISION"
    ERROR = "ERROR"
    RECOVERY_EVENT = "RECOVERY_EVENT"
