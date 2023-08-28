from fastapi import APIRouter, Depends

from app.dependencies.deps import authorize_api
from app.api.v1.api import router as api_router
from app.api.v1.chart import router as chart_router
from app.api.v1.email import router as email_router
from app.api.v1.frontend import router as frontend_router
from app.api.v1.user import router as user_router
from app.api.v1.role import router as role_router
from app.api.v1.log import router as log_router
from app.api.v1.member import router as member_router

router = APIRouter(prefix='/v1')

router.include_router(api_router, dependencies=[Depends(authorize_api)])
router.include_router(chart_router, dependencies=[Depends(authorize_api)])
router.include_router(user_router)  # 局部授權
router.include_router(email_router, dependencies=[Depends(authorize_api)])
router.include_router(frontend_router, dependencies=[Depends(authorize_api)])
router.include_router(role_router, dependencies=[Depends(authorize_api)])
router.include_router(log_router, dependencies=[Depends(authorize_api)])
router.include_router(member_router, dependencies=[Depends(authorize_api)])
