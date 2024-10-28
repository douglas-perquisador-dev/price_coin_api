# tests/test_strategies.py
import pytest
from unittest.mock import AsyncMock
from app.services.strategies import MercadoBitcoinStrategy, FallbackStrategy
from datetime import datetime


@pytest.mark.asyncio
async def test_mercado_bitcoin_fetch(mocker):
    # Mock do fetch_client
    # mock_fetch_client = mocker.patch("app.core.utils.fetch_client", new_callable=AsyncMock)

    # Simulando os dados retornados pela API
    mock_fetch_client = {
            "response_data": {
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
            },
            "BTCUSD": {
                "bid": 90000
            }
        }


    strategy = MercadoBitcoinStrategy()
    result = await strategy._parse_data(mock_fetch_client)

    # Verifica se o resultado está correto
    assert result["coin_name"] == "Bitcoin"
    assert result["symbol"] == "BTC"
    assert result["coin_price"] == 50000
    assert result["coin_price_dolar"] == "90000"
    assert "date_consult" in result


@pytest.mark.asyncio
async def test_fallback_fetch(mocker):
    # Mock do fetch_client
    mock_fetch_client = mocker.patch("app.core.utils.fetch_client", new_callable=AsyncMock)

    # Simulando os dados retornados pela API
    mock_fetch_client.side_effect = [
        {
            "code": "BTC",
            "bid": 49000,
            "name": "Bitcoin/BRL",
            "create_date": "2024-10-28"
        },
        {
            "BTCUSD": {
                "bid": 90000
            }
        }
    ]

    strategy = FallbackStrategy()
    result = await strategy.fetch("BTC")

    # Verifica se o resultado está correto
    assert result["coin_name"] == "Bitcoin"
    assert result["symbol"] == "BTC"
    assert result["coin_price"] == 49000
    assert result["coin_price_dolar"] == "90000"
    assert result["date_consult"] == "2024-10-28"

