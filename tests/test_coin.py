import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.main import app
from app.services.strategies import  FallbackStrategy
import time

cryptocurrencies = {
    "Bitcoin": "BTC",
    "Ethereum": "ETH",
    "Binance Coin": "BNB",
    "Ripple": "XRP",
    "Litecoin": "LTC",
    "Cardano": "ADA",
    "Polkadot": "DOT",
    "Chainlink": "LINK",
    "Dogecoin": "DOGE",
    "Solana": "SOL",
    "Avalanche": "AVAX",
    "Polygon": "MATIC",
    "Shiba Inu": "SHIB",
    "Uniswap": "UNI",
    "Terra": "LUNA",
    "Algorand": "ALGO",
    "VeChain": "VET",
    "Cosmos": "ATOM",
    "Monero": "XMR",
    "Tezos": "XTZ",
    "Filecoin": "FIL",
    "Zcash": "ZEC",
    "Stellar": "XLM",
    "EOS": "EOS",
    "TRON": "TRX",
    "Aave": "AAVE",
    "Compound": "COMP",
    "SushiSwap": "SUSHI",
    "Maker": "MKR",
    "Fantom": "FTM",
}

# Inicializando o cache no FastAPI para os testes
@pytest.fixture(autouse=True)
def setup_cache():
    # Configura o backend de cache para os testes
    cache_backend = RedisBackend("redis://localhost:6379")  # ou usar MemoryBackend para testes locais
    FastAPICache.init(cache_backend)
    yield  # Aqui é onde o teste é executado
    # Aqui você pode adicionar o que precisa após o teste, como limpar o cache

client = TestClient(app)

@pytest.fixture
def mock_coin_provider(mocker):
    # Cria o mock do provedor de moedas
    mock_provider = mocker.Mock()
    return mock_provider


@pytest.mark.asyncio
async def test_get_coin_info_fallback(mocker, mock_coin_provider):
    # Mocking o provedor de fallback
    mock_fetch_client = mocker.patch('app.core.utils.fetch_client', autospec=True)

    # Dados mockados para as duas chamadas fetch_client
    # Simulando a resposta do preço em BRL para o símbolo BTC
    mock_fetch_client.side_effect = [
        {'data': {'BTC': {'name': 'Bitcoin', 'symbol': 'BTC', 'quote': {'BRL': {'price': 388788.33}}}}},  # BRL
        {'data': {'BTC': {'quote': {'USD': {'price': 388788.33}}}}}  # USD
    ]


    response = client.post("/coin_infos", json={"symbol": "BTC"}, auth=("admin", "123456"))

    assert response.status_code == 200
    # Verifica se os campos de atributos estão presentes na resposta
    assert set(response.json().keys()) == {"coin_name", "symbol", "coin_price", "coin_price_dolar", "date_consult"}


@pytest.mark.asyncio
async def test_get_major_coins_info(mocker, mock_coin_provider):
	for coin_name, coin_symbol in cryptocurrencies.items():
		response = client.post("/coin_infos", json={"symbol": coin_symbol}, auth=("admin", "123456"))

		if response.status_code == 404:
			# Aguarda 2 segundos
			time.sleep(5)
			response = client.post("/coin_infos", json={"symbol": coin_symbol}, auth=("admin", "123456"))

		if response.status_code == 200:
			print(f"Sucesso para {coin_name} ({coin_symbol}) - Status 200")
		elif response.status_code == 400:
			print(f"Erro para {coin_name} ({coin_symbol}) - Status 400")
		else:
			print(f"Status não esperado para {coin_name} ({coin_symbol}) - Status {response.status_code}")

		# Verifica se os campos de atributos estão presentes na resposta
		# assert response.status_code in [200, 400]  # Esperando 200 ou 400
		if response.status_code == 200:
			assert set(response.json().keys()) == {"coin_name", "symbol", "coin_price", "coin_price_dolar",
												   "date_consult"}


@pytest.mark.asyncio
async def test_get_major_coins_info2(mocker, mock_coin_provider):
	for coin_name, coin_symbol in cryptocurrencies.items():
		# response = client.post("/coin_infos", json={"symbol": coin_symbol}, auth=("admin", "123456"))

		# Instância da estratégia FallbackStrategy
		strategy = FallbackStrategy()

		try:
			response = await strategy.fetch(coin_symbol)
		except:
			# Aguarda 2 segundos
			time.sleep(5)
			response = await strategy.fetch(coin_symbol)

		res_success = set(response.keys()) == {"coin_name", "symbol", "coin_price", "coin_price_dolar",
												   "date_consult"}
		res_error = set(response.keys()) == {"detail"}

		if res_success:
			print(f"Sucesso para {coin_name} ({coin_symbol}) - Status 200")
		elif res_error:
			print(f"Error para {coin_name} ({coin_symbol}) - Status 400")
		else:
			print(f"Status não esperado para {coin_name} ({coin_symbol}) - Status {response.status_code}")

		# Verifica se os campos de atributos estão presentes na resposta
		# assert response.status_code in [200, 400]  # Esperando 200 ou 400