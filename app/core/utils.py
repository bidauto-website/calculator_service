from pathlib import Path

import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
def init_fastapi_cache(custom_redis_client = None):
    if not custom_redis_client:
        redis_client = redis.Redis.from_url(settings.REDIS_URL)
    else:
        redis_client = custom_redis_client
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")