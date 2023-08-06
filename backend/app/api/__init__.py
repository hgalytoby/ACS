from fastapi import APIRouter

from app.api.v1 import router as v1_router
from app.api.accept import router as accept_router
from app.api.oauth import router as oauth_router
from app.schemas.health import health_read, HealthRead

router = APIRouter()

router.include_router(v1_router)
router.include_router(accept_router)
router.include_router(oauth_router)


@router.get('/health')
async def health() -> HealthRead:
    return health_read


try:
    from app.api.test import router as test_router

    router.include_router(test_router)
except ImportError:
    ...
