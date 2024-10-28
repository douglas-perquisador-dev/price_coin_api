from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.models.coin import CoinRequest

security = HTTPBasic()


def authenticate_user(func):
    async def wrapper(coin: CoinRequest, credentials: HTTPBasicCredentials = Depends(security)):
        correct_username = "admin"
        correct_password = "123456"

        if credentials.username == correct_username and credentials.password == correct_password:
            return await func(coin)  # Passa apenas o parâmetro coin para a função
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais incorretas",
                headers={"WWW-Authenticate": "Basic"},
            )

    return wrapper
