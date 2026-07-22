from typing import Protocol

from packages.prediction.domain.models import Prediction


class PredictionRepository(Protocol):
    """Port Ä‘á»‹nh nghÄ©a cÃ¡c hÃ nh vi lÆ°u trá»¯ vÃ  truy váº¥n dá»± Ä‘oÃ¡n."""

    def save(self, pred: Prediction) -> Prediction: ...

    def find_by_id(self, pred_id: str) -> Prediction | None: ...

    def list_all(self) -> list[Prediction]: ...

