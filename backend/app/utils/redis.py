import redis.asyncio as redis

from app.core.config import settings


async def init_redis_pool() -> redis.Redis:
    return await redis.from_url(
        url=settings.redis.url,
        encoding='utf-8',
        decode_responses=True,
    )
