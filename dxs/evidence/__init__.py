"""DXS Evidence lifecycle boundary.

Provides:
- Evidence model
- Evidence capture service
- Immutable hash generation
- Evidence ledger storage
- Governance timeline tracking
"""

from .hash import EvidenceHasher, calculate_hash
from .ledger import EvidenceLedger
from .model import Evidence, EvidenceStatus
from .service import EvidenceService
from .timeline import EvidenceTimeline, TimelineEvent

__all__ = [
    "Evidence",
    "EvidenceHasher",
    "EvidenceLedger",
    "EvidenceService",
    "EvidenceStatus",
    "EvidenceTimeline",
    "TimelineEvent",
    "calculate_hash",
]
