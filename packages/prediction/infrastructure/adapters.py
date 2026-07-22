from packages.prediction.domain.models import Prediction
from packages.prediction.domain.ports import PredictionRepository


class InMemoryPredictionRepository(PredictionRepository):
    """Adapter lÆ°u trá»¯ káº¿t quáº£ dá»± Ä‘oÃ¡n trong RAM phá»¥c vá»¥ kiá»ƒm thá»­."""

    def __init__(self) -> None:
        self._store: dict[str, Prediction] = {}

    def save(self, pred: Prediction) -> Prediction:
        self._store[pred.id] = pred
        return pred

    def find_by_id(self, pred_id: str) -> Prediction | None:
        return self._store.get(pred_id)

    def list_all(self) -> list[Prediction]:
        return list(self._store.values())

