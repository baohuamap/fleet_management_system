from aioredis import Redis, from_url

from app.config import settings


def cache():
    return Redis(host=settings.redis_server, port=settings.redis_port)


redis = from_url("redis://redis-cache:6379")
