from fastapi_cache.decorator import cache
from functools import wraps

def cache_result(expire: int = 60):
    def decorator(func):
        @wraps(func)
        @cache(expire=expire)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator
