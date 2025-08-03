#!/bin/bash

# Script para configurar deploy automático via Git hooks

echo "=== CONFIGURAÇÃO DE DEPLOY AUTOMÁTICO ==="
echo "Data/Hora: $(date)"
echo "========================================"

# Verificar se estamos em um repositório Git
if [ ! -d ".git" ]; then
    echo "❌ Erro: Não estamos em um repositório Git"
    exit 1
fi

# Criar diretório hooks se não existir
if [ ! -d ".git/hooks" ]; then
    echo "📁 Criando diretório .git/hooks..."
    mkdir -p .git/hooks
fi

# Criar o hook post-commit
echo "🔧 Criando hook post-commit..."
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash

# Hook post-commit para deploy automático
# Este script é executado automaticamente após cada commit

echo "=== HOOK POST-COMMIT: DEPLOY AUTOMÁTICO ==="
echo "Data/Hora: $(date)"
echo "=========================================="

# Verificar se estamos no branch main
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "⚠️  Não estamos no branch main ($CURRENT_BRANCH). Pulando deploy automático."
    exit 0
fi

echo "✅ Branch main detectado. Iniciando deploy automático..."

# Fazer push para o repositório remoto
echo "🚀 Fazendo push para o repositório..."
git push

# Chamar URL de deploy
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
    echo "✅ Deploy automático iniciado com sucesso!"
else
    echo "❌ Erro no deploy automático. Código HTTP: $HTTP_CODE"
    echo "⚠️  O commit foi realizado, mas o deploy falhou."
    echo "💡 Execute manualmente: ./deploy_force.sh"
fi

echo "=== HOOK POST-COMMIT CONCLUÍDO ==="
echo "Data/Hora: $(date)"
echo "=================================="
EOF

# Tornar o hook executável
chmod +x .git/hooks/post-commit

echo "✅ Hook post-commit configurado com sucesso!"
echo ""
echo "📋 Configuração:"
echo "   - Deploy automático ativado"
echo "   - Só funciona no branch main"
echo "   - Executa após cada commit"
echo "   - Faz push e chama URL de deploy"
echo ""
echo "🧪 Para testar, faça um commit:"
echo "   git add ."
echo "   git commit -m 'teste: deploy automático'"
echo ""
echo "📝 Logs aparecerão após o commit" 