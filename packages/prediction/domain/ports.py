from typing import Protocol

from packages.prediction.domain.models import Prediction


class PredictionRepository(Protocol):
    """Port định nghĩa các hành vi lưu trữ và truy vấn dự đoán."""

    def save(self, pred: Prediction) -> Prediction: ...

    def find_by_id(self, pred_id: str) -> Prediction | None: ...

    def list_all(self) -> list[Prediction]: ...