# db/redis_client.py
import redis.asyncio as redis
from config import REDIS_URL

_redis_client = None

async def get_redis():
    """Lazy singleton Redis connection."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10
        )
    return _redis_client
