import os
from contextlib import asynccontextmanager
from arq import create_pool
from arq.connections import RedisSettings
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db

from app.api import router
from app.core.config import settings, logger
from app.crud import crud_user
from app.db.session import engine
from app.utils.redis import init_redis_pool
from app.websocket import broadcast, router as ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.isdir('static'):
        os.mkdir('static')

    logger.info('程式啟動! 如果無法訪問請確認 Redis 有沒有啟動成功!')

    await broadcast.connect()

    async with db():
        first_user = await crud_user.get_first_created_at_user()

    items = {
        'initial_time': first_user.created_at,
        'arq': await create_pool(RedisSettings(host=settings.redis.host)),
        'redis': init_redis_pool(),
        'db': db,
    }

    yield items

    await items['redis'].close()
    await broadcast.disconnect()


app = FastAPI(
    debug=not settings.is_prod,
    docs_url='/docs' if not settings.is_prod else None,
    lifespan=lifespan,
)

app.add_middleware(
    SQLAlchemyMiddleware,
    custom_engine=engine,
)

if settings.is_dev:
    # 測試的時候才加 DebugToolbarMiddleware，因為變成同步的了速度會變慢，。
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=['app.db.session.SQLAlchemyPanel'],
    )
    app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(router, prefix='/api')
app.include_router(ws_router)


@app.get('/')
async def docs() -> RedirectResponse:
    return RedirectResponse(app.docs_url)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'app.main:app',
        host=settings.server_host,
        port=int(settings.server_port),
        reload=True,
        proxy_headers=True,
        forwarded_allow_ips='*',
    )
