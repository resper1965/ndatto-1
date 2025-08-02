# Use uma imagem Python oficial como base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Define variáveis de ambiente para evitar que o Python escreva arquivos .pyc e buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo requirements.txt e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY . .

# Cria um usuário não-root para segurança
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expõe a porta que a aplicação Flask irá rodar
EXPOSE 5000

# Comando para executar a aplicação
CMD ["python", "app.py"]
