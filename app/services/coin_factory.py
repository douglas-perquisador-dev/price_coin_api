from app.services.strategies import MercadoBitcoinStrategy, FallbackStrategy

class CoinProviderFactory:
    @staticmethod
    def get_provider(provider_name: str):
        if provider_name == "mercado_bitcoin":
            return MercadoBitcoinStrategy()
        elif provider_name == "fallback":
            return FallbackStrategy()
        else:
            raise ValueError("Provedor de API inválido")
