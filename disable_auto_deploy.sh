#!/bin/bash

# Script para desabilitar deploy automático

echo "=== DESABILITAR DEPLOY AUTOMÁTICO ==="
echo "Data/Hora: $(date)"
echo "===================================="

# Verificar se o hook existe
if [ ! -f ".git/hooks/post-commit" ]; then
    echo "⚠️  Hook post-commit não encontrado. Deploy automático já está desabilitado."
    exit 0
fi

# Fazer backup do hook atual
echo "💾 Fazendo backup do hook atual..."
cp .git/hooks/post-commit .git/hooks/post-commit.backup

# Remover o hook
echo "🗑️  Removendo hook post-commit..."
rm .git/hooks/post-commit

echo "✅ Deploy automático desabilitado com sucesso!"
echo ""
echo "📋 Status:"
echo "   - Hook post-commit removido"
echo "   - Backup salvo em .git/hooks/post-commit.backup"
echo "   - Commits não farão mais deploy automático"
echo ""
echo "🔄 Para reabilitar, execute:"
echo "   ./setup_auto_deploy.sh"
echo ""
echo "📝 Para restaurar o backup:"
echo "   cp .git/hooks/post-commit.backup .git/hooks/post-commit"
echo "   chmod +x .git/hooks/post-commit" 