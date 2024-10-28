# Use uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho na imagem
WORKDIR /app

# Copia o arquivo de requisitos para a imagem
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para a imagem
COPY . .

# Expõe a porta padrão do FastAPI
EXPOSE 8000

# Comando para iniciar o aplicativo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
