import redis.asyncio as redis

from app.core.config import settings


def init_redis_pool() -> redis.Redis:
    return redis.from_url(
        url=settings.redis.url,
        encoding='utf-8',
        decode_responses=True,
    )
