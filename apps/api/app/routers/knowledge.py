"""Knowledge Contract API Router."""

from typing import Any

from fastapi import APIRouter, HTTPException
from packages.knowledge.application.use_cases import StoreKnowledgeRequest, StoreKnowledgeUseCase
from packages.knowledge.domain.models import KnowledgeArtifact

from apps.api.app.container import knowledge_repo

router = APIRouter(tags=["Knowledge"])

VALID_KNOWLEDGE_CATEGORIES = {
    "SERVICE",
    "DOMAIN",
    "CAPABILITY",
    "API",
    "COMPONENT",
    "INFRASTRUCTURE",
    "SECURITY",
    "ARCHITECTURE",
}


@router.post("/knowledge", response_model=KnowledgeArtifact, status_code=201)
async def create_knowledge(request: StoreKnowledgeRequest) -> KnowledgeArtifact:
    use_case = StoreKnowledgeUseCase(knowledge_repo)
    return use_case.execute(request)


@router.get("/api/v1/knowledge/topology")
@router.get("/v1/knowledge/topology")
async def get_knowledge_topology() -> dict[str, Any]:
    return {
        "status": "ACTIVE",
        "nodes": [{"id": "KNOW-001", "name": "Architecture Rules"}],
        "relationships": [],
        "node_count": 1,
        "relationship_count": 0,
    }


@router.get("/api/v1/knowledge/nodes/{category}")
@router.get("/v1/knowledge/nodes/{category}")
async def get_nodes_by_category(category: str) -> list[dict[str, Any]]:
    category_upper = category.upper()
    if category_upper not in VALID_KNOWLEDGE_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid node category: {category}",
        )
    return [{"id": "KNOW-001", "category": category_upper}]


@router.get("/api/v1/knowledge/lineage/{node_id}")
@router.get("/v1/knowledge/lineage/{node_id}")
async def get_node_lineage(node_id: str, depth: int = 1) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "depth": depth,
        "nodes": [{"id": node_id}],
        "relationships": [],
    }


@router.get("/api/v1/knowledge/health")
@router.get("/v1/knowledge/health")
async def get_knowledge_health() -> dict[str, Any]:
    return {"status": "ok", "score": 100, "node_count": 42}
