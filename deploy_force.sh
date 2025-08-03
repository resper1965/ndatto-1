#!/bin/bash

# Script de Deploy Forçado
# Este script sempre faz commit e deploy, mesmo sem mudanças

set -e  # Para o script se houver erro

echo "=== DEPLOY FORÇADO ==="
echo "Data/Hora: $(date)"
echo "======================"

# 1. Adicionar Dockerfile ao git (força adição mesmo sem mudanças)
echo "📦 Adicionando Dockerfile ao git..."
git add Dockerfile

# 2. Fazer commit (força commit mesmo sem mudanças)
echo "💾 Fazendo commit..."
COMMIT_MESSAGE="deploy: forçar atualização Dockerfile - $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MESSAGE" || {
    echo "⚠️  Nenhuma mudança para commitar, mas continuando..."
    # Se não há mudanças, cria um commit vazio
    git commit --allow-empty -m "$COMMIT_MESSAGE"
}

# 3. Fazer push
echo "🚀 Fazendo push para o repositório..."
git push

# 4. Chamar URL de deploy
echo "🌐 Chamando URL de deploy..."
DEPLOY_URL="http://62.72.8.164:3000/api/deploy/deddad00ec3e4fc63c63f76d2005c2259f9dbd682a9eeb4f"

# Usar curl para chamar a URL de deploy
echo "📡 Fazendo requisição para: $DEPLOY_URL"
RESPONSE=$(curl -s -w "\n%{http_code}" "$DEPLOY_URL")

# Separar resposta e código HTTP
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | head -n -1)

echo "📡 Resposta do deploy:"
echo "Código HTTP: $HTTP_CODE"
echo "Resposta: $RESPONSE_BODY"

# Verificar se o deploy foi bem-sucedido
if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 202 ]; then
    echo "✅ Deploy iniciado com sucesso!"
else
    echo "❌ Erro no deploy. Código HTTP: $HTTP_CODE"
    echo "Tentando novamente em 5 segundos..."
    sleep 5
    
    # Segunda tentativa
    RESPONSE=$(curl -s -w "\n%{http_code}" "$DEPLOY_URL")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    RESPONSE_BODY=$(echo "$RESPONSE" | head -n -1)
    
    echo "📡 Segunda tentativa - Resposta:"
    echo "Código HTTP: $HTTP_CODE"
    echo "Resposta: $RESPONSE_BODY"
    
    if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 202 ]; then
        echo "✅ Deploy iniciado com sucesso na segunda tentativa!"
    else
        echo "❌ Falha no deploy após duas tentativas"
        exit 1
    fi
fi

echo "=== DEPLOY CONCLUÍDO ==="
echo "Data/Hora: $(date)"
echo "========================" 