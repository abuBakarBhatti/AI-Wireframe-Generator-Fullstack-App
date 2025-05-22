import time
from typing import Optional
import redis
import json
from functools import lru_cache
from pydantic import BaseModel

from app.config import settings


class SimpleCache:
    """A simple in-memory cache implementation."""
    
    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl
        
    def get(self, key: str) -> Optional[dict]:
        """Get a value from the cache."""
        if key in self.cache:
            value, expiry = self.cache[key]
            if expiry > time.time():
                return value
            else:
                del self.cache[key]
        return None
        
    def set(self, key: str, value: dict) -> None:
        """Set a value in the cache."""
        expiry = time.time() + self.ttl
        self.cache[key] = (value, expiry)

@lru_cache()
def get_cache():
    """
    Get the cache implementation based on configuration.
    
    Returns:
        Cache implementation or None if caching is disabled
    """
    if not settings.CACHE_ENABLED:
        return None
        
    # Use simple in-memory cache for now
    # This could be extended to use Redis or other cache backends
    return SimpleCache(ttl=settings.CACHE_TTL)
