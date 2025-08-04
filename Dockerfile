# Dockerfile otimizado para produção
# Aplicação NCISO - Sistema de Monitoramento de Dispositivos
# Versão: 1.2.1 - Janeiro 2025
# Status: Sem autenticação - Redirecionamento /login corrigido
# Domínio: ndatto.ncsio.ness.tec.br

# Use uma imagem Python oficial como base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Define variáveis de ambiente para otimização
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000
ENV BASE_URL=https://ndatto.ncsio.ness.tec.br

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copia o arquivo requirements.txt e instala as dependências Python
# Isso otimiza o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia apenas os arquivos necessários para a aplicação
COPY app.py .
COPY data_collector.py .
COPY supabase_client.py .
COPY templates/ templates/
COPY static/ static/

# Cria um usuário não-root para segurança
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expõe a porta que a aplicação Flask irá rodar
EXPOSE 5000

# Health check para verificar se a aplicação está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Comando para executar a aplicação em produção
CMD ["python", "app.py"]
