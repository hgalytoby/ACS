from fastapi import APIRouter, Request

from app.schemas.health import HealthRead

router = APIRouter()


@router.get('/health')
async def health(request: Request) -> HealthRead:
    return HealthRead(client_ip=request.client.host)
