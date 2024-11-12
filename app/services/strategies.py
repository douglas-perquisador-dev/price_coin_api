from datetime import datetime
from app.core.config import settings
from fastapi import HTTPException, status
from app.core.utils import fetch_client, get_coin


class CoinFetchStrategy:
    def __init__(self, provider):
        self.provider = provider

    async def fetch_coin_price(self, symbol: str):
        return await self.provider.fetch(symbol)

class MercadoBitcoinStrategy:
    async def fetch(self, symbol: str):
        url = f"{settings.mercado_bitcoin_url}?symbol={symbol}&limit=20"
        url_usd = f"{settings.fallback_url}{symbol}-usd"


        data_coin = await fetch_client(url)
        if not data_coin:
            return data_coin

        data_coin["coin_price_dolar"] = (await fetch_client(url_usd))[f"{symbol.upper()}USD"]["bid"]
        return self._parse_data(data_coin)

    def _parse_data(self, data):
        product = data["response_data"]["products"][0]
        return {
            "coin_name": product["name"],
            "symbol": product["product_data"]["symbol"],
            "coin_price": float(product["market_price"]),
            "coin_price_dolar": str(data["coin_price_dolar"]),
            "date_consult": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

class FallbackStrategy:
    async def fetch(self, symbol: str):
        try:

            url_brl = f"{settings.fallback_url}?symbol={symbol.lower()}&convert=brl"
            url_usd = f"{settings.fallback_url}?symbol={symbol.lower()}&convert=usd"

            data_coin = (await fetch_client(url_brl, True))['data'][f"{symbol.upper()}"]
            data_coin["coin_price_dolar"] = (await fetch_client(url_usd, True))['data'][f"{symbol.upper()}"]["quote"]["USD"]["price"]
            return self._parse_data(data_coin)
        except Exception as e:
            print(">>> Error: ", e)
            # Se a moeda não for encontrada, lança uma exceção HTTP
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Moeda com símbolo '{symbol}' não encontrada."
            )

    def _parse_data(self, data):
        return {
            "coin_name": str(data['name']),
            "symbol": data["symbol"],
            "coin_price": data["quote"]["BRL"]["price"],
            "coin_price_dolar": str(data["coin_price_dolar"]),
            "date_consult": datetime.now()
        }
