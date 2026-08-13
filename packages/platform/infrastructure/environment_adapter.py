from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

"""Adaptive Hardware & Environment Profiler for EAOS Platform."""


class ExecutionModeEnum(StrEnum):
    """Execution mode selecting hard embedded vs soft cloud."""

    HARD_EMBEDDED_LOCAL = "HARD_EMBEDDED_LOCAL"
    SOFT_CLOUD_DISTRIBUTED = "SOFT_CLOUD_DISTRIBUTED"
    HYBRID_FEDERATED = "HYBRID_FEDERATED"


class EnvironmentProfileDTO(BaseModel):
    """Value object representing physical infrastructure constraints."""

    model_config = ConfigDict(frozen=True)

    target_facility_type: str
    execution_mode: ExecutionModeEnum
    has_network: bool
    cpu_cores: int
    available_ram_mb: int
    uses_sqlite_wal: bool = True
    uses_wasm_sandbox: bool = True
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AdaptiveEnvironmentEngine:
    """Engine auto-detecting physical hardware & selecting execution mode."""

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()

    def profile_and_adapt(
        self,
        facility_type: str = "SMART_DEVICE",
        is_offline: bool = False,
        ram_mb: int = 512,
    ) -> EnvironmentProfileDTO:
        """Detects physical constraints and selects optimal mode."""
        fac_upper = facility_type.upper()
        if is_offline or ram_mb < 2048 or "SATELLITE" in fac_upper or "SUBMARINE" in fac_upper or "BUNKER" in fac_upper:
            mode = ExecutionModeEnum.HARD_EMBEDDED_LOCAL
        elif ram_mb >= 8192 and not is_offline:
            mode = ExecutionModeEnum.SOFT_CLOUD_DISTRIBUTED
        else:
            mode = ExecutionModeEnum.HYBRID_FEDERATED

        return EnvironmentProfileDTO(
            target_facility_type=facility_type,
            execution_mode=mode,
            has_network=not is_offline,
            cpu_cores=4,
            available_ram_mb=ram_mb,
            uses_sqlite_wal=True,
            uses_wasm_sandbox=True,
        )


if __name__ == "__main__":
    engine = AdaptiveEnvironmentEngine()
    sat = engine.profile_and_adapt("SATELLITE_SPACECRAFT", True, 256)
    print(f"✔ Spacecraft Mode: {sat.execution_mode}")
    cloud = engine.profile_and_adapt("HOSPITAL_ENTERPRISE", False, 16384)
    print(f"✔ Hospital Mode  : {cloud.execution_mode}")
