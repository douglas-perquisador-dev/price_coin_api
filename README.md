# Price Coin API

Este projeto é uma API desenvolvida com **FastAPI** que permite consultar informações sobre criptomoedas, como preços e dados relacionados. A API está configurada para ser executada em um ambiente Docker, facilitando a instalação e o uso.

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas na sua máquina:

- **Docker**: [Instruções de instalação](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Instruções de instalação](https://docs.docker.com/compose/install/)

## Instalação

 **Clone o repositório**:

```bash
   git clone https://github.com/seu_usuario/preco_coin_api.git
   cd preco_coin_api
```

### 1. Instalação de Dependências

Certifique-se de ter o **Docker** e o **Docker Compose** instalados na sua máquina.

### 2. Executar a API

No diretório raiz do projeto, basta rodar o comando abaixo para construir e iniciar os containers necessários:

**Linux/MacOS**
```bash
make api
```

**Windows**
```bash
docker compose up -d --build
```

Isso irá subir a aplicação, juntamente com todos os serviços necessários, como o Redis.

A API estará disponível em: `http://localhost:8000`.

### 3. Autenticação

Para acessar as rotas protegidas da API, você precisará usar as seguintes credenciais:

- **Usuário**: `admin`
- **Senha**: `123456`


## Testando a API

Você pode testar a API utilizando ferramentas como o **Insomnia** ou **cURL**. Abaixo está um exemplo de como realizar uma chamada autenticada:
### Exemplo de uso com cURL
```bash
curl --location 'http://localhost:8000/coin_infos' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic dXNlcl8xOnNlbmhhMTIz' \
--data '{
    "symbol": "BTC"
  }'
```
**Nota**: O valor dXNlcl8xOnNlbmhhMTIz é a string codificada em Base64 para admin:123456. Você pode gerar essa string usando o seguinte comando:

## Observação
Devido ao Cloudflare CDN bloquear meu IP com base na API v1, meu acesso foi limitado à url https://store.mercadobitcoin.com.br/api/v1/marketplace/product/unlogged. 