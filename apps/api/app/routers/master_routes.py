from fastapi import APIRouter

from apps.api.app.routers.autonomous import router as autonomous_router
from apps.api.app.routers.capability_runtime import router as capability_router
from apps.api.app.routers.events_chaos import router as events_chaos_router
from apps.api.app.routers.federation import router as federation_router
from apps.api.app.routers.governance import router as governance_router
from apps.api.app.routers.health import router as health_router
from apps.api.app.routers.intelligence import router as intelligence_router
from apps.api.app.routers.knowledge import router as knowledge_router
from apps.api.app.routers.memory_knowledge import router as memory_router
from apps.api.app.routers.security import router as security_router
from apps.api.app.routers.telemetry_performance import router as telemetry_router
from apps.api.app.routers.tenancy import router as tenancy_router

"""Master Router aggregating all sub-routers for apps/api."""


master_router = APIRouter()

master_router.include_router(health_router)
master_router.include_router(knowledge_router)
master_router.include_router(memory_router)
master_router.include_router(governance_router)
master_router.include_router(security_router)
master_router.include_router(telemetry_router)
master_router.include_router(events_chaos_router)
master_router.include_router(federation_router)
master_router.include_router(tenancy_router)
master_router.include_router(intelligence_router)
master_router.include_router(autonomous_router)
master_router.include_router(capability_router)
