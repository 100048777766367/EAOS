"""Operating model registry mapping organization, roles, and value streams."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class ValueStreamDTO(BaseModel):
    """Value object representing an enterprise value stream."""

    model_config = ConfigDict(frozen=True)

    stream_id: str
    name: str
    owner: str
    status: str


class OperatingModelRegistry:
    """Registry managing enterprise roles, services, and value streams."""

    STREAMS: tuple[str, ...] = (
        "architecture_governance",
        "capability_delivery",
        "autonomous_evolution",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.op_dir: Path = self.root_dir / "operating_model"

    def discover_value_streams(self) -> list[ValueStreamDTO]:
        """Discovers active enterprise value streams."""
        return [
            ValueStreamDTO(
                stream_id=f"val_{stream}",
                name=stream.replace("_", " ").title(),
                owner="Chief Enterprise Architect",
                status="ACTIVE",
            )
            for stream in self.STREAMS
        ]
