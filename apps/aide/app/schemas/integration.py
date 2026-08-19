"""AIDE integration schemas."""

from pydantic import BaseModel, ConfigDict


class GatewayProbe(BaseModel):
    """Observed Gateway connectivity from the AIDE boundary."""

    model_config = ConfigDict(frozen=True)

    target: str
    status: str
    detail: str
