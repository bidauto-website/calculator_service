import json
from typing import Callable, Any

from redis.asyncio import Redis

from app.config import settings

class Cache:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL)

    async def set_cache(self, key: str, value: Any, ttl: int = 900):
        if isinstance(value, (bytes, bytearray)):
            data = bytes(value)
        elif isinstance(value, (int, float)):
            data = str(value).encode("utf-8")
        elif isinstance(value, str):
            data = value.encode("utf-8")
        else:
            data = json.dumps(value, ensure_ascii=False).encode("utf-8")
        await self.redis.set(key, data, ex=ttl)

    async def get_cache(self, key: str):
        return await self.redis.get(key)
    @staticmethod
    def _normalize(value: Any) -> Any:
        if isinstance(value, (bytes, bytearray)):
            try:
                s = value.decode("utf-8")
            except Exception:
                return value
        elif isinstance(value, str):
            s = value
        else:
            return value
        try:
            return json.loads(s)
        except Exception:
            try:
                if s.isdigit() or (s.startswith("-") and s[1:].isdigit()):
                    return int(s)
                return float(s)
            except Exception:
                return s

    async def get_or_set_cache(self, key: str, value_func: Callable[[], Any], ttl: int = 900):
        cached = await self.redis.get(key)
        if cached is not None:
            return self._normalize(cached)
        value = await value_func()
        await self.set_cache(key, value, ttl)
        return self._normalize(value)
