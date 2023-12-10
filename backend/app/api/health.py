from fastapi import APIRouter

from app.schemas.health import HealthRead, health_read

router = APIRouter()


@router.get('/health')
async def health() -> HealthRead:
    return health_read
