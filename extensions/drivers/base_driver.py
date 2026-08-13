from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

"""Base Driver Protocol for Hardware and Infrastructure Drivers."""


class DriverStatusDTO(BaseModel):
    """Value object representing driver operational status."""

    model_config = ConfigDict(frozen=True)

    driver_id: str = Field(..., description="Driver ID e.g. drv-waf")
    name: str = Field(..., description="Driver name")
    hardware_target: str = Field(default="CPU")
    is_active: bool = Field(default=True)


@runtime_checkable
class BaseRuntimeDriver(Protocol):
    """Protocol defining the contract for all runtime drivers."""

    driver_id: str
    name: str

    def initialize_driver(self) -> bool: ...

    def get_driver_status(self) -> DriverStatusDTO: ...
