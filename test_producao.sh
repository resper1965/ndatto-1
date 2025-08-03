#!/bin/bash

echo "🧪 TESTE DA APLICAÇÃO EM PRODUÇÃO"
echo "=================================="
echo ""

# 1. Teste de conectividade básica
echo "1️⃣ Testando conectividade básica..."
echo "   URL: http://62.72.8.164:3000"
curl -s -o /dev/null -w "   Status: %{http_code}\n" http://62.72.8.164:3000/

echo ""

# 2. Teste da API Flask (porta 5000)
echo "2️⃣ Testando API Flask (porta 5000)..."
echo "   URL: http://62.72.8.164:5000"
curl -s -o /dev/null -w "   Status: %{http_code}\n" http://62.72.8.164:5000/

echo ""

# 3. Teste de endpoints específicos
echo "3️⃣ Testando endpoints específicos..."

echo "   Testando /api/health..."
curl -s -w "   Status: %{http_code}\n" http://62.72.8.164:5000/api/health

echo "   Testando /api/devices..."
curl -s -w "   Status: %{http_code}\n" http://62.72.8.164:5000/api/devices

echo ""

# 4. Verificar status do container
echo "4️⃣ Verificando status do container..."
ssh -o StrictHostKeyChecking=no root@62.72.8.164 "cd /etc/easypanel/projects/nciso/nciso-dattormm/code && docker ps | grep dattormm"

echo ""

# 5. Verificar logs recentes
echo "5️⃣ Logs recentes da aplicação..."
ssh -o StrictHostKeyChecking=no root@62.72.8.164 "cd /etc/easypanel/projects/nciso/nciso-dattormm/code && docker logs \$(docker ps -q --filter 'name=dattormm' | head -1) --tail 5"

echo ""
echo "✅ Teste concluído!" 