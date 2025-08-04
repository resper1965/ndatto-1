#!/bin/bash

# Script para fazer commit e push para o GitHub
# Sistema NCISO - Monitoramento de Dispositivos

set -e  # Para o script se houver erro

echo "🚀 Iniciando deploy para GitHub..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verifica se estamos no diretório correto
if [ ! -f "app.py" ]; then
    print_error "Não estamos no diretório correto do projeto!"
    exit 1
fi

print_status "Verificando status do Git..."

# Verifica se há mudanças para commitar
if git diff --quiet && git diff --cached --quiet; then
    print_warning "Não há mudanças para commitar!"
    echo "Arquivos modificados:"
    git status --porcelain
    exit 0
fi

# Mostra arquivos que serão commitados
print_status "Arquivos modificados:"
git status --porcelain

echo ""
print_status "Adicionando arquivos ao Git..."

# Adiciona todos os arquivos (exceto os ignorados)
git add .

# Verifica se há arquivos para commitar
if git diff --cached --quiet; then
    print_warning "Nenhum arquivo foi adicionado (todos estão no .gitignore)"
    exit 0
fi

# Gera mensagem de commit com timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MESSAGE="feat: Integração completa com API Datto RMM

- Criado data_collector.py para coleta de dados da API Datto
- Implementado sistema de testes com test_datto_api.py
- Atualizado dashboard para exibir dados reais
- Adicionado endpoints /sync e /test-collector
- Melhorado templates para mostrar dispositivos e alertas
- Atualizado requirements.txt com dependências necessárias
- Criada documentação completa da API Datto

Timestamp: $TIMESTAMP"

print_status "Fazendo commit com mensagem:"
echo "$COMMIT_MESSAGE"
echo ""

# Faz o commit
if git commit -m "$COMMIT_MESSAGE"; then
    print_success "Commit realizado com sucesso!"
else
    print_error "Erro ao fazer commit!"
    exit 1
fi

# Verifica se há um remote configurado
if ! git remote get-url origin > /dev/null 2>&1; then
    print_warning "Remote 'origin' não configurado!"
    echo "Para configurar, use:"
    echo "git remote add origin https://github.com/resper1965/ndatto-1.git"
    exit 0
fi

# Mostra informações do remote
print_status "Remote configurado:"
git remote -v

echo ""
print_status "Fazendo push para o GitHub..."

# Tenta fazer o push
if git push origin main; then
    print_success "Push realizado com sucesso!"
    print_success "Código enviado para o GitHub!"
else
    print_error "Erro ao fazer push!"
    echo "Possíveis causas:"
    echo "- Branch não existe no remote"
    echo "- Problemas de autenticação"
    echo "- Conflitos de merge"
    echo ""
    echo "Para criar a branch main no remote:"
    echo "git push -u origin main"
    exit 1
fi

echo ""
print_success "✅ Deploy concluído com sucesso!"
print_status "Próximos passos:"
echo "1. Configure as variáveis de ambiente no EasyPanel:"
echo "   - Vá para Settings > Environment Variables"
echo "   - Adicione DATTO_API_KEY e DATTO_API_SECRET"
echo "2. Execute: python test_datto_api.py"
echo "3. Acesse a aplicação e teste a sincronização"
echo "4. Verifique o dashboard com dados reais"
echo ""
echo "📋 Documentação:"
echo "- EASYPANEL_ENV_SETUP.md - Configuração do EasyPanel"
echo "- DATTO_API_SETUP.md - Configuração da API Datto"
echo "- AVALIACAO_SISTEMA.md - Avaliação completa do sistema"

echo ""
print_status "📊 Resumo das mudanças:"
git log --oneline -1 