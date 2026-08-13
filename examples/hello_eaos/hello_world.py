from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Hello EAOS Executable Example."""


class HelloEAOSResultDTO(BaseModel):
    """Result DTO for Hello EAOS example execution."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(default="SUCCESS")
    greeting: str = Field(default="Welcome to EAOS Centennial Edition")
    constitution_version: str = Field(default="3.0")


def run_hello_eaos_example() -> HelloEAOSResultDTO:
    """Execute Hello EAOS starter example."""
    return HelloEAOSResultDTO(
        status="SUCCESS",
        greeting="Welcome to Enterprise Architecture Operating System",
        constitution_version="3.0",
    )
