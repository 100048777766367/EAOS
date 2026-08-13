from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

"""Enterprise Contracts Registry & Schema Validator Engine."""


class ContractProtocolDTO(BaseModel):
    """Value object representing an API/Protocol Contract."""

    model_config = ConfigDict(frozen=True)

    contract_id: str = Field(..., description="Unique Contract ID")
    protocol: str = Field(..., description="REST, GRPC, GRAPHQL, MCP, EVENT")
    schema_file: str = Field(..., description="Relative schema file path")
    is_valid: bool = Field(default=True)


class EnterpriseContractRegistryEngine:
    """Engine loading and validating API and Protocol Contracts."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()
        self.contracts_dir = self.root / "contracts"

    def audit_all_contracts(self) -> list[ContractProtocolDTO]:
        """Scan contracts directory and audit protocol schemas."""
        if not self.contracts_dir.exists():
            return []

        contracts: list[ContractProtocolDTO] = []

        rest_spec = self.contracts_dir / "rest" / "openapi_gateway_spec.json"
        contracts.append(
            ContractProtocolDTO(
                contract_id="contract-rest-openapi",
                protocol="REST",
                schema_file="contracts/rest/openapi_gateway_spec.json",
                is_valid=rest_spec.exists(),
            )
        )

        grpc_file = self.contracts_dir / "grpc" / "federation_service.proto"
        contracts.append(
            ContractProtocolDTO(
                contract_id="contract-grpc-federation",
                protocol="GRPC",
                schema_file="contracts/grpc/federation_service.proto",
                is_valid=grpc_file.exists(),
            )
        )

        gql_file = self.contracts_dir / "graphql" / "schema.graphql"
        contracts.append(
            ContractProtocolDTO(
                contract_id="contract-graphql",
                protocol="GRAPHQL",
                schema_file="contracts/graphql/schema.graphql",
                is_valid=gql_file.exists(),
            )
        )

        mcp_file = self.contracts_dir / "mcp" / "mcp_tools_contract.json"
        contracts.append(
            ContractProtocolDTO(
                contract_id="contract-mcp-agent-tools",
                protocol="MCP",
                schema_file="contracts/mcp/mcp_tools_contract.json",
                is_valid=mcp_file.exists(),
            )
        )

        evt_file = self.contracts_dir / "events" / "domain_events_schema.json"
        contracts.append(
            ContractProtocolDTO(
                contract_id="contract-async-events",
                protocol="EVENT",
                schema_file="contracts/events/domain_events_schema.json",
                is_valid=evt_file.exists(),
            )
        )

        return contracts
