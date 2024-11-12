import aiohttp
from app.core.config import settings

async def fetch_client(url: str, is_api_key: bool = False):
    headers = {
        "User-Agent": "fastapi",
        "Accept": "application/json",
    }
    if is_api_key:
        headers["X-CMC_PRO_API_KEY"] = settings.api_key

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


# Função assíncrona para obter o ID de uma moeda usando o símbolo
async def get_coin(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

    headers = {
        'X-CMC_PRO_API_KEY': settings.api_key,
        'Accept': 'application/json'
    }

    params = {
        'symbol': symbol.upper()
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            data = await response.json()
            if 'data' in data and data['data']:
                coin = data['data'][0]
                return coin['id']  # Retorna o ID da moeda
            return None