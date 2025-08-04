# Documentação do Sistema NCISO

Este diretório contém toda a documentação do sistema de monitoramento NCISO.

## 📚 Documentação Principal

### 🚀 **Configuração e Deploy**
- **[DATTO_API_SETUP.md](DATTO_API_SETUP.md)** - Configuração da API Datto RMM
- **[EASYPANEL_ENV_SETUP.md](EASYPANEL_ENV_SETUP.md)** - Configuração de variáveis no EasyPanel
- **[DOMAIN_SETUP.md](DOMAIN_SETUP.md)** - Configuração de domínio personalizado

### 📊 **Avaliação e Resumo**
- **[AVALIACAO_SISTEMA.md](AVALIACAO_SISTEMA.md)** - Avaliação completa do sistema
- **[RESUMO_IMPLEMENTACAO.md](RESUMO_IMPLEMENTACAO.md)** - Resumo da implementação realizada

## 🔧 Scripts Disponíveis

### 📁 **Diretório `/scripts`**
- **`deploy_production.sh`** - Script de deploy em produção
- **`test_datto_api.py`** - Teste da API Datto (na raiz)

### 📁 **Diretório `/config`**
- **`production.env`** - Exemplo de variáveis de ambiente para produção

## 📋 Estrutura do Projeto

```
nciso/
├── app.py                 # Aplicação principal Flask
├── data_collector.py      # Coletor de dados da API Datto
├── supabase_client.py     # Cliente Supabase
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
├── deploy_to_github.sh   # Script de deploy automatizado
├── docs/                 # Documentação
│   ├── README.md         # Este arquivo
│   ├── DATTO_API_SETUP.md
│   ├── EASYPANEL_ENV_SETUP.md
│   ├── AVALIACAO_SISTEMA.md
│   ├── RESUMO_IMPLEMENTACAO.md
│   └── DOMAIN_SETUP.md
├── scripts/              # Scripts de automação
│   └── deploy_production.sh
├── config/               # Arquivos de configuração
│   └── production.env
├── static/               # Arquivos estáticos
└── templates/            # Templates HTML
```

## 🎯 Guias Rápidos

### 1. **Configuração Inicial**
1. Leia [EASYPANEL_ENV_SETUP.md](EASYPANEL_ENV_SETUP.md)
2. Configure as variáveis no EasyPanel
3. Teste com [DATTO_API_SETUP.md](DATTO_API_SETUP.md)

### 2. **Deploy**
1. Use `./deploy_to_github.sh` para commit e push
2. O deploy automático será iniciado
3. Verifique logs no EasyPanel

### 3. **Testes**
1. Execute `python test_datto_api.py`
2. Acesse `/test-collector` na aplicação
3. Verifique dashboard com dados reais

## 📞 Suporte

- **Email**: resper@ness.com.br
- **Repositório**: https://github.com/resper1965/ndatto-1
- **Documentação**: Este diretório

---

**Última Atualização**: Janeiro 2025  
**Versão**: 1.0.0 