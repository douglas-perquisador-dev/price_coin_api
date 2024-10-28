from pydantic import BaseModel
from datetime import datetime

# Define a estrutura da requisição recebida
class CoinRequest(BaseModel):
    symbol: str

# Define a estrutura da resposta enviada
class CoinResponse(BaseModel):
    coin_name: str
    symbol: str
    coin_price: float
    coin_price_dolar: str
    date_consult: datetime
