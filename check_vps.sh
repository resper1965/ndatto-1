#!/bin/bash

# Script para verificar status da aplicação na VPS

VPS_IP="62.72.8.164"
APP_PATH="/etc/easypanel/projects/nciso/nciso-dattormm/code"

echo "=== VERIFICAÇÃO DA APLICAÇÃO NA VPS ==="
echo "IP: $VPS_IP"
echo "Caminho: $APP_PATH"
echo "====================================="

# 1. Verificar variáveis de ambiente
echo ""
echo "1. Verificando variáveis de ambiente..."
ssh -o StrictHostKeyChecking=no root@$VPS_IP "cd $APP_PATH && env | grep SUPABASE"

# 2. Verificar se a aplicação está rodando
echo ""
echo "2. Verificando containers Docker..."
ssh -o StrictHostKeyChecking=no root@$VPS_IP "docker ps | grep -i dattormm"

# 3. Verificar logs da aplicação
echo ""
echo "3. Verificando logs da aplicação..."
ssh -o StrictHostKeyChecking=no root@$VPS_IP "docker logs \$(docker ps -q --filter 'name=dattormm') --tail 20"

# 4. Verificar arquivos da aplicação
echo ""
echo "4. Verificando arquivos da aplicação..."
ssh -o StrictHostKeyChecking=no root@$VPS_IP "ls -la $APP_PATH"

# 5. Verificar se há arquivo .env na VPS
echo ""
echo "5. Verificando arquivo .env na VPS..."
ssh -o StrictHostKeyChecking=no root@$VPS_IP "ls -la $APP_PATH/.env 2>/dev/null || echo 'Arquivo .env não encontrado'"

echo ""
echo "=== VERIFICAÇÃO CONCLUÍDA ===" 