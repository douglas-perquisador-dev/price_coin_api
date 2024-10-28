import httpx
from fastapi import APIRouter, Depends
import asyncio

from app.services.coin_factory import CoinProviderFactory
from app.decorators.cache_decorator import cache_result
from app.decorators.auth_decorator import authenticate_user
from app.services.strategies import CoinFetchStrategy
from app.models.coin import CoinRequest, CoinResponse

router = APIRouter()


@router.post("/coin_infos", response_model=CoinResponse)
@authenticate_user  # Aplica o decorator de autenticação
@cache_result(expire=20) # Depois, cache por 60 segundos
async def get_coin_info(coin: CoinRequest):
    # Obtenha o provedor através do Factory Method
    provider = CoinProviderFactory.get_provider("mercado_bitcoin")
    # request_client = httpx.AsyncClient()

    # Usar a estratégia de busca de dados
    strategy = CoinFetchStrategy(provider)
    result = await strategy.fetch_coin_price(coin.symbol.lower())

    if result:
        return result
    else:
        provider = CoinProviderFactory.get_provider("fallback")
        strategy = CoinFetchStrategy(provider)
        # await asyncio.sleep(2)
        return await strategy.fetch_coin_price(coin.symbol.lower())