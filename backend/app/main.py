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
from app.core.config import settings
from app.crud import crud_user
from app.db.session import engine
from app.utils.enums import AppEnv
from app.utils.redis import init_redis_pool
from app.websocket import broadcast, router as ws_router

is_dev = settings.app_env == AppEnv.DEVELOPMENT


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.isdir('static'):
        os.mkdir('static')
    async with db():
        first_user = await crud_user.get_first_created_at_user()
    items = {
        'initial_time': first_user.created_at,
        'arq': await create_pool(RedisSettings(host=settings.redis.host)),
        'redis': await init_redis_pool(),
        'db': db,
    }
    await broadcast.connect()
    yield items
    await items['redis'].close()
    await broadcast.disconnect()


app = FastAPI(
    debug=is_dev,
    docs_url='/docs' if is_dev else None,
    lifespan=lifespan,
)
app.add_middleware(
    DebugToolbarMiddleware,
    panels=['app.db.session.SQLAlchemyPanel'],
)
app.add_middleware(
    SQLAlchemyMiddleware,
    custom_engine=engine,
)

if is_dev:
    app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(router, prefix='/api')
app.include_router(ws_router)


@app.get('/')
async def docs():
    return RedirectResponse(app.docs_url)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'app.main:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
