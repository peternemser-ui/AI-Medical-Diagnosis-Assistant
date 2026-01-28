from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import hashlib
import json
from functools import wraps


class CacheEntry:
    """Represents a cached value with expiration."""

    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(seconds=ttl_seconds)

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at


class CacheService:
    """In-memory caching service with TTL support."""

    def __init__(self, default_ttl: int = 300):
        """Initialize cache with default TTL in seconds."""
        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl
        self._stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0
        }

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        entry = self._cache.get(key)

        if entry is None:
            self._stats['misses'] += 1
            return None

        if entry.is_expired:
            del self._cache[key]
            self._stats['misses'] += 1
            return None

        self._stats['hits'] += 1
        return entry.value

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """Set value in cache with optional TTL."""
        ttl = ttl or self._default_ttl
        self._cache[key] = CacheEntry(value, ttl)
        self._stats['sets'] += 1

    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if key in self._cache:
            del self._cache[key]
            self._stats['deletes'] += 1
            return True
        return False

    async def exists(self, key: str) -> bool:
        """Check if key exists and is not expired."""
        entry = self._cache.get(key)
        if entry is None or entry.is_expired:
            return False
        return True

    async def clear(self) -> int:
        """Clear all cached values."""
        count = len(self._cache)
        self._cache.clear()
        return count

    async def clear_expired(self) -> int:
        """Clear only expired entries."""
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.is_expired
        ]

        for key in expired_keys:
            del self._cache[key]

        return len(expired_keys)

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self._stats['hits'] + self._stats['misses']
        hit_rate = self._stats['hits'] / total_requests if total_requests > 0 else 0

        return {
            **self._stats,
            'total_requests': total_requests,
            'hit_rate': round(hit_rate * 100, 2),
            'current_size': len(self._cache)
        }

    def reset_stats(self) -> None:
        """Reset cache statistics."""
        self._stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0
        }

    @staticmethod
    def make_key(*args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True, default=str)
        return hashlib.md5(key_data.encode()).hexdigest()


def cached(ttl: int = 300, key_prefix: str = ''):
    """Decorator for caching function results."""
    def decorator(func):
        cache = CacheService(default_ttl=ttl)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{CacheService.make_key(*args, **kwargs)}"

            # Try to get from cache
            result = await cache.get(cache_key)
            if result is not None:
                return result

            # Call function and cache result
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl)

            return result

        # Expose cache for manual operations
        wrapper.cache = cache

        return wrapper
    return decorator


# Specialized caches for different data types
class DrugCache(CacheService):
    """Cache for drug information lookups."""

    def __init__(self):
        super().__init__(default_ttl=3600)  # 1 hour

    async def get_drug(self, rxcui: str) -> Optional[Dict]:
        """Get cached drug info."""
        return await self.get(f"drug:{rxcui}")

    async def set_drug(self, rxcui: str, drug_info: Dict) -> None:
        """Cache drug info."""
        await self.set(f"drug:{rxcui}", drug_info)

    async def get_interactions(self, drug_ids: tuple) -> Optional[Dict]:
        """Get cached drug interactions."""
        key = f"interactions:{':'.join(sorted(drug_ids))}"
        return await self.get(key)

    async def set_interactions(self, drug_ids: tuple, interactions: Dict) -> None:
        """Cache drug interactions."""
        key = f"interactions:{':'.join(sorted(drug_ids))}"
        await self.set(key, interactions, ttl=1800)  # 30 minutes


class DiagnosisCache(CacheService):
    """Cache for diagnosis results."""

    def __init__(self):
        super().__init__(default_ttl=1800)  # 30 minutes

    async def get_similar_diagnosis(self, symptoms_hash: str) -> Optional[Dict]:
        """Get cached diagnosis for similar symptoms."""
        return await self.get(f"diagnosis:{symptoms_hash}")

    async def set_diagnosis(self, symptoms_hash: str, diagnosis: Dict) -> None:
        """Cache diagnosis result."""
        await self.set(f"diagnosis:{symptoms_hash}", diagnosis)

    @staticmethod
    def hash_symptoms(symptoms: list, severity: int = None) -> str:
        """Generate hash for symptom set."""
        data = {
            'symptoms': sorted([s.lower().strip() for s in symptoms]),
            'severity': severity
        }
        return hashlib.sha256(json.dumps(data).encode()).hexdigest()[:16]


# Global cache instances
drug_cache = DrugCache()
diagnosis_cache = DiagnosisCache()
general_cache = CacheService()
