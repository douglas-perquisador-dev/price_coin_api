import redis.asyncio as redis
from pydantic_settings import BaseSettings
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import os

class Settings(BaseSettings):
    mercado_bitcoin_url: str = os.getenv("MERCADO_BTC_URL", "https://store.mercadobitcoin.com.br/api/v1/marketplace/product/unlogged")
    fallback_url: str = os.getenv("FALLBACK_URL", "https://economia.awesomeapi.com.br/last/")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Settings()

# Função de inicialização do cache
async def startup_cache():
    redis_instance = redis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis_instance), prefix="fastapi-cache")
