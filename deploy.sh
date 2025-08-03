#!/bin/bash

# Script de Deploy Automatizado
# Este script faz commit do Dockerfile e chama a URL de deploy

set -e  # Para o script se houver erro

echo "=== DEPLOY AUTOMATIZADO ==="
echo "Data/Hora: $(date)"
echo "=========================="

# 1. Verificar se há mudanças no Dockerfile
if git diff --quiet Dockerfile; then
    echo "❌ Nenhuma mudança detectada no Dockerfile"
    echo "Saindo sem fazer deploy..."
    exit 0
fi

echo "✅ Mudanças detectadas no Dockerfile"

# 2. Adicionar Dockerfile ao git
echo "📦 Adicionando Dockerfile ao git..."
git add Dockerfile

# 3. Fazer commit
echo "💾 Fazendo commit..."
COMMIT_MESSAGE="deploy: atualizar Dockerfile - $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MESSAGE"

# 4. Fazer push
echo "🚀 Fazendo push para o repositório..."
git push

# 5. Chamar URL de deploy
echo "🌐 Chamando URL de deploy..."
DEPLOY_URL="http://62.72.8.164:3000/api/deploy/deddad00ec3e4fc63c63f76d2005c2259f9dbd682a9eeb4f"

# Usar curl para chamar a URL de deploy
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
    exit 1
fi

echo "=== DEPLOY CONCLUÍDO ==="
echo "Data/Hora: $(date)"
echo "==========================" 