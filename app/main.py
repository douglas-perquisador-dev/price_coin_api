from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.api.endpoints import router
from app.core.config import startup_cache
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o cache ao iniciar o app
    await startup_cache()
    yield  # O ponto em que a aplicação começa a rodar
    # Aqui você pode colocar lógica de desligamento, se necessário

app = FastAPI(title="Coin Price API", version="1.0", lifespan=lifespan)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Define os domínios permitidos
    allow_credentials=True,            # Permite o envio de cookies e headers de autenticação
    allow_methods=["*"],               # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],               # Permite todos os headers
)

# Registro dos endpoints
app.include_router(router)
