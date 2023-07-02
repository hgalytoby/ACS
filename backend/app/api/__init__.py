from fastapi import APIRouter

from app.api.v1 import router as v1_router
from app.api.accept import router as accept_router
from app.api.oauth import router as oauth_router

router = APIRouter()

router.include_router(v1_router)
router.include_router(accept_router)
router.include_router(oauth_router)

try:
    from app.api.test import router as test_router

    router.include_router(test_router)
except ImportError:
    ...
