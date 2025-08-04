#!/bin/bash

# Script de Deploy para Produção
# NCISO - Sistema de Monitoramento de Dispositivos

set -e  # Para o script se houver erro

echo "=== DEPLOY DE PRODUÇÃO NCISO ==="
echo "Data/Hora: $(date)"
echo "================================"

# Configurações
VPS_IP="62.72.8.164"
APP_PATH="/etc/easypanel/projects/nciso/nciso-dattormm/code"
DEPLOY_URL="http://62.72.8.164:3000/api/deploy/deddad00ec3e4fc63c63f76d2005c2259f9dbd682a9eeb4f"

# 1. Verificar se há mudanças
echo "📋 Verificando mudanças..."
if git diff --quiet; then
    echo "⚠️  Nenhuma mudança detectada"
    read -p "Continuar mesmo assim? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Deploy cancelado"
        exit 0
    fi
fi

# 2. Adicionar todos os arquivos
echo "📦 Adicionando arquivos..."
git add -A

# 3. Fazer commit
echo "💾 Fazendo commit..."
COMMIT_MESSAGE="deploy: produção NCISO - $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MESSAGE"

# 4. Fazer push
echo "🚀 Fazendo push para o repositório..."
git push

# 5. Chamar URL de deploy
echo "🌐 Chamando URL de deploy..."
RESPONSE=$(curl -s -w "\n%{http_code}" "$DEPLOY_URL")

# Separar resposta e código HTTP
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | head -n -1)

echo "📡 Resposta do deploy:"
echo "Código HTTP: $HTTP_CODE"
echo "Resposta: $RESPONSE_BODY"

# 6. Verificar se o deploy foi bem-sucedido
if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 202 ]; then
    echo "✅ Deploy iniciado com sucesso!"
    
    # 7. Aguardar um pouco e verificar status
    echo "⏳ Aguardando 30 segundos para verificar status..."
    sleep 30
    
    # 8. Verificar status da aplicação
    echo "🔍 Verificando status da aplicação..."
    ssh -o StrictHostKeyChecking=no root@$VPS_IP "cd $APP_PATH && docker ps | grep dattormm" || {
        echo "⚠️  Container não encontrado, tentando novamente..."
        sleep 10
        ssh -o StrictHostKeyChecking=no root@$VPS_IP "cd $APP_PATH && docker ps | grep dattormm"
    }
    
    # 9. Verificar logs
    echo "📝 Verificando logs..."
    ssh -o StrictHostKeyChecking=no root@$VPS_IP "cd $APP_PATH && docker logs \$(docker ps -q --filter 'name=dattormm' | head -1) --tail 10"
    
else
    echo "❌ Erro no deploy. Código HTTP: $HTTP_CODE"
    echo "💡 Tentando novamente em 10 segundos..."
    sleep 10
    
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

echo ""
echo "=== DEPLOY DE PRODUÇÃO CONCLUÍDO ==="
echo "Data/Hora: $(date)"
echo "Status: ✅ SUCESSO"
echo "================================" 