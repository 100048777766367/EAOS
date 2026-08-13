# EAOS API & Protocol Contracts Package (`contracts/`)

## Business Capability
Published API & Protocol Contracts Management, Interface Isolation, and Multi-Protocol Schema Registry (REST, gRPC, GraphQL, MCP, Async Events).

## Package Structure
- `events/`: Async Domain Event JSON Schemas (`domain_events_schema.json`).
- `graphql/`: GraphQL Query/Mutation Schemas (`schema.graphql`).
- `grpc/` & `proto/`: High-Performance Protobuf Schemas (`federation_service.proto`, `governance_v1.proto`).
- `mcp/`: Model Context Protocol AI Tool Calling Schemas (`mcp_tools_contract.json`).
- `rest/` & `openapi/`: OpenAPI 3.1 REST Gateway Contracts (`openapi_gateway_spec.json`).
- `contract_registry.py`: Master Contract Registry Engine & Schema Auditor.
