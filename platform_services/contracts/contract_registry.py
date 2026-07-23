"""Contract registry and single-source-of-truth contract loader for EAOS."""

from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class ContractMetadataDTO(BaseModel):
    """Value object representing communication contract metadata."""

    model_config = ConfigDict(frozen=True)

    contract_id: str
    protocol_type: str
    file_path: str
    version: str


class ContractRegistry:
    """Registry scanning and verifying communication contracts across protocols."""

    PROTOCOL_MAP: ClassVar[dict[str, str]] = {
        "events": "ASYNC_EVENT_SCHEMA",
        "graphql": "GRAPHQL_SCHEMA",
        "grpc": "GRPC_PROTOBUF",
        "mcp": "MODEL_CONTEXT_PROTOCOL",
        "rest": "OPENAPI_SPEC",
    }

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.contracts_dir: Path = self.root_dir / "contracts"

    def discover_contracts(self) -> list[ContractMetadataDTO]:
        """Scans contracts subdirectories and returns discovered contracts."""
        results: list[ContractMetadataDTO] = []
        if not self.contracts_dir.exists():
            return results

        for proto_dir in self.contracts_dir.iterdir():
            if proto_dir.is_dir() and not proto_dir.name.startswith("."):
                proto_type = self.PROTOCOL_MAP.get(proto_dir.name, "GENERIC_CONTRACT")
                file_items = [f for f in proto_dir.iterdir() if f.is_file() and not f.name.startswith(".")]
                results.extend(
                    ContractMetadataDTO(
                        contract_id=file_path.stem,
                        protocol_type=proto_type,
                        file_path=str(file_path.relative_to(self.root_dir)),
                        version="1.0.0",
                    )
                    for file_path in file_items
                )

        return results
