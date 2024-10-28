# tests/test_coin.py
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Importa o aplicativo FastAPI
from app.models.coin import CoinRequest
from app.services.strategies import MercadoBitcoinStrategy

client = TestClient(app)


@pytest.fixture
def mock_coin_provider(mocker):
    # Cria o mock do provedor de moedas
    mock_provider = mocker.Mock()
    return mock_provider


@pytest.mark.asyncio
async def test_get_coin_info_success(mocker, mock_coin_provider):
    mock_provider = mocker.Mock(spec=MercadoBitcoinStrategy)
    mock_provider.fetch.return_value = {
        "response_data": {
		"total_items": 1,
		"products": [
			{
				"product_id": "BTC",
				"name": "Bitcoin",
				"icon_url": {
					"svg": "https://static.mercadobitcoin.com.br/web/img/icons/assets/ico-asset-btc-color.svg",
					"png": "https://static.mercadobitcoin.com.br/app/general/assets/btc.png"
				},
				"type": "crypto",
				"market_price": "388788.33000000000000000000000000000000",
				"tags": [],
				"description": "Bitcoin é uma moeda digital que permite pagamentos em transações online sem a necessidade de um intermediário. Baseada na rede blockchain, foi a pioneira entre as criptomoedas.",
				"product_data": {
					"symbol": "BTC",
					"type": "crypto",
					"sub_type": {
						"code": "coin",
						"display_text": "Criptomoeda"
					},
					"variation": {
						"string": "+0.72%",
						"number": 0.7165295810981192,
						"status": "positive"
					},
					"market_cap": "7671288667305.76300000000000000000000000000000",
					"created_at": "2022-08-29T07:04:49",
					"release_date": "2013-01-01",
					"asset_decimals": 8,
					"fiat_decimals": 2,
					"visible_when_unlogged": True,
					"visible_when_logged": True,
					"prelisted": False,
					"fact_sheet_url": None,
					"term_url": None,
					"warnings": [],
					"cover_letter_data": {
						"cover_letter_additional_info": "",
						"show_cover_letter_chart": True,
						"show_cover_letter": True
					},
					"origin_groups_allowed": None,
					"contract_type": "",
					"payment_type": "",
					"visibility_filter_tags": [
						"public"
					],
					"quote": "BRL"
				},
				"favorite": False,
				"balances": {
					"available_quantity": "0",
					"available_fiat_value": "0",
					"on_hold_quantity": "0",
					"on_hold_fiat_value": "0",
					"wallet_details": []
				},
				"visible_when_logged": True,
				"visible_when_unlogged": True
			}
		],
		"pagination": {
			"limit": 20,
			"offset": 0
		}
	}
    }

    mocker.patch("app.services.coin_factory.CoinProviderFactory.get_provider", return_value=mock_coin_provider)

    # Realiza a requisição
    response = client.post("/coin_infos", json={"symbol": "BTC"})

    assert response.status_code == 200
    # Verifica se os campos de atributos estão presentes na resposta
    assert set(response.json().keys()) == {"coin_name", "symbol", "coin_price", "coin_price_dolar", "date_consult"}


@pytest.mark.asyncio
async def test_get_coin_info_fallback(mocker, mock_coin_provider):
    # Mocking o provedor de fallback
    mock_fallback_provider = mocker.Mock()
    mock_fallback_provider.fetch.side_effect = [
        None,  # Primeira tentativa falha
        {
            "name": "Bitcoin",
            "code": "BTC",
            "bid": 49000,
            "coin_price_dolar": "90000",
            "create_date": "2024-10-28"
        }
    ]

    mocker.patch("app.services.coin_factory.CoinProviderFactory.get_provider",
                 side_effect=[mock_coin_provider, mock_fallback_provider])

    response = client.post("/coin_infos", json={"symbol": "BTC"})

    assert response.status_code == 200
    # Verifica se os campos de atributos estão presentes na resposta
    assert set(response.json().keys()) == {"coin_name", "symbol", "coin_price", "coin_price_dolar", "date_consult"}
