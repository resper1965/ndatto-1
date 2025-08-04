# n.secops - Sistema de Monitoramento de Dispositivos

Sistema de monitoramento e gerenciamento de dispositivos baseado em Flask e Supabase, com integração completa com a API do Datto RMM.

## 🚀 Status do Projeto

✅ **Integração com API Datto RMM** - Sistema completo de coleta de dados  
✅ **Dashboard em Tempo Real** - Visualização de dispositivos e alertas  
✅ **Sistema de Testes** - Validação da conectividade com a API  
✅ **Documentação Completa** - Guias de configuração e uso  

## 📊 Funcionalidades Principais

- 🔍 **Monitoramento de Dispositivos** - Status, hardware, localização
- 🚨 **Sistema de Alertas** - Notificações em tempo real
- 📍 **Gestão de Sites** - Organização por localização
- 📈 **Dashboard Interativo** - Estatísticas e métricas
- 🔄 **Sincronização Automática** - Dados sempre atualizados
- 🧪 **Sistema de Testes** - Validação da API Datto

## 🚀 Configuração Rápida

### 1. Variáveis de Ambiente

#### Para Desenvolvimento Local

Crie um arquivo `.env` na raiz do projeto:

```bash
# Supabase Configuration
SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
SUPABASE_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX
SUPABASE_SECRET=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW

# Datto RMM API
DATTO_API_KEY=sua-chave-api-datto-aqui
DATTO_API_SECRET=seu-segredo-api-datto-aqui

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
```

#### Para Produção (EasyPanel)

**Configuração no EasyPanel:**
1. Acesse o painel do EasyPanel
2. Vá para o projeto `nciso-dattormm`
3. Navegue até **Settings** > **Environment Variables**
4. Adicione as seguintes variáveis:

**Variáveis Obrigatórias:**
```bash
SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzemZxcW1tbGpla2libWNnbWlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE5NDE4NTAsImV4cCI6MjA2NzUxNzg1MH0.y5-XyIFRpBX8uolv6IzvcNHs0_Xm6Q3eV74YFc_Vc6s
SUPABASE_SECRET=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzemZxcW1tbGpla2libWNnbWlnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTk0MTg1MCwiZXhwIjoyMDY3NTE3ODUwfQ.LL99WTJPqiTQNViTduyi8r5itQSkaw1b9Gomv58Ajyk
SECRET_KEY=nciso-prod-2025-secure-key-change-in-production
FLASK_APP=app.py
FLASK_ENV=production
```

**Variáveis da API Datto:**
```bash
DATTO_API_KEY=sua-chave-real-api-datto
DATTO_API_SECRET=seu-segredo-real-api-datto
```

**Nota:** As variáveis de ambiente no EasyPanel são persistidas automaticamente e ficam disponíveis para a aplicação em produção.

**Docker Compose:**
```yaml
version: '3.8'
services:
  app:
    build: .
    environment:
      - SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
      - SUPABASE_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX
      - SUPABASE_SECRET=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW
      - SECRET_KEY=your-production-secret-key-here
      - FLASK_APP=app.py
      - FLASK_ENV=production
    ports:
      - "5000:5000"
```

**Docker Run:**
```bash
docker run -d \
  -e SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co \
  -e SUPABASE_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX \
  -e SUPABASE_SECRET=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW \
  -e SECRET_KEY=your-production-secret-key-here \
  -e FLASK_APP=app.py \
  -e FLASK_ENV=production \
  -p 5000:5000 \
  your-app-image
```

### 2. Instalação Local

```bash
# Clone o repositório
git clone https://github.com/resper1965/ndatto-1.git
cd ndatto-1

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure o arquivo .env (veja acima)

# Execute a aplicação
python app.py

# Acesse diretamente
http://localhost:5000
```

### 3. Build Docker

```bash
# Build da imagem
docker build -t nsecops .

# Execute com variáveis de ambiente
docker run -d \
  -e SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co \
  -e SUPABASE_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX \
  -e SUPABASE_SECRET=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW \
  -e SECRET_KEY=your-production-secret-key-here \
  -p 5000:5000 \
  nsecops
```

## 📋 Variáveis de Ambiente

### Obrigatórias

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `SUPABASE_URL` | URL do projeto Supabase | `https://pszfqqmmljekibmcgmig.supabase.co` |
| `SUPABASE_KEY` | Chave pública do Supabase | `sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX` |
| `SUPABASE_SECRET` | Chave secreta do Supabase | `sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW` |
| `SECRET_KEY` | Chave secreta do Flask | `your-secret-key-here` |

### Opcionais

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `FLASK_APP` | Arquivo principal da aplicação | `app.py` |
| `FLASK_ENV` | Ambiente Flask | `development` |
| `DATTO_API_KEY` | Chave da API Datto RMM | - |
| `DATTO_API_SECRET` | Segredo da API Datto RMM | - |

## 🔧 Configuração do Supabase

### 1. Obter as Chaves

1. Acesse o [Supabase Dashboard](https://supabase.com/dashboard)
2. Selecione seu projeto
3. Vá para **Settings** > **API**
4. Copie as chaves:
   - **URL**: `https://pszfqqmmljekibmcgmig.supabase.co`
   - **Publishable key**: `sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX`
   - **Secret key**: `sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW`

### 2. Configurar Tabelas

Execute os seguintes comandos SQL no Supabase:

```sql
-- Tabela de dispositivos
CREATE TABLE devices (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hostname TEXT,
    site_uid TEXT,
    status TEXT DEFAULT 'offline',
    ip_address INET,
    last_seen TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de alertas
CREATE TABLE alerts (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_uid UUID REFERENCES devices(uid),
    alert_type TEXT,
    severity TEXT DEFAULT 'low',
    status TEXT DEFAULT 'new',
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de sites
CREATE TABLE sites (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT,
    address TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de componentes de dispositivos
CREATE TABLE device_components (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_uid UUID REFERENCES devices(uid),
    name TEXT,
    type TEXT,
    status TEXT DEFAULT 'unknown',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de logs de auditoria
CREATE TABLE audit_logs (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action TEXT,
    entity_type TEXT,
    entity_id TEXT,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🚨 Troubleshooting

### Erro: "Invalid API key"

**Causa:** Variáveis de ambiente não configuradas corretamente.

**Solução:**
1. Verifique se as variáveis estão definidas:
   ```bash
   echo $SUPABASE_URL
   echo $SUPABASE_KEY
   ```

2. Em produção, configure as variáveis no sistema de deploy

3. Verifique se está usando a chave correta:
   - Use a **Publishable key** para operações normais
   - Use a **Secret key** apenas para operações administrativas

### Erro: "Module not found"

**Causa:** Dependências não instaladas.

**Solução:**
```bash
pip install -r requirements.txt
```

### Erro: "Permission denied"

**Causa:** Problemas de permissão no Docker.

**Solução:**
```bash
sudo chown -R $USER:$USER .
```

## 📁 Estrutura do Projeto

```
nciso/
├── app.py                 # Aplicação principal Flask
├── data_collector.py      # Coletor de dados da API Datto
├── supabase_client.py     # Cliente Supabase
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
├── deploy_to_github.sh   # Script de deploy automatizado
├── test_datto_api.py     # Teste da API Datto
├── postman_collection.json # Coleção Postman para API Datto
├── .gitignore           # Arquivos ignorados pelo Git
├── docs/                # Documentação
│   ├── README.md        # Documentação organizada
│   ├── DATTO_API_SETUP.md
│   ├── EASYPANEL_ENV_SETUP.md
│   ├── POSTMAN_SETUP.md # Configuração Postman
│   ├── AVALIACAO_SISTEMA.md
│   ├── RESUMO_IMPLEMENTACAO.md
│   └── DOMAIN_SETUP.md
├── scripts/             # Scripts de automação
│   └── deploy_production.sh
├── config/              # Arquivos de configuração
│   └── production.env
├── static/              # Arquivos estáticos
│   ├── css/
│   └── js/
└── templates/           # Templates HTML
    ├── base.html
    ├── dashboard.html
    ├── login.html
    └── ...
```

## 🧪 Testando a API Datto

### 1. Teste Básico
```bash
python test_datto_api.py
```

### 2. Teste via Interface Web
1. Acesse a aplicação diretamente
2. Navegue para `/test-collector`

### 3. Sincronização Manual
```bash
# Via curl
curl -X GET https://seu-dominio.com/sync

# Ou acesse /sync na aplicação
```

## 🔐 Segurança

- **Nunca** commite o arquivo `.env` no Git
- Use chaves diferentes para desenvolvimento e produção
- Configure Row Level Security (RLS) no Supabase
- Use HTTPS em produção
- Troque a `SECRET_KEY` em produção
- **Proteja as chaves da API Datto** - Nunca exponha em logs ou commits

## 🚀 Deploy

### Deploy Automático
```bash
# Execute o script de deploy
./deploy_to_github.sh
```

### Deploy Manual
```bash
# Adicione arquivos
git add .

# Faça commit
git commit -m "feat: Integração com API Datto"

# Push para GitHub
git push origin main
```

### Deploy Docker
```bash
# Build da imagem
docker build -t nsecops .

# Execute
docker run -d \
  -e SUPABASE_URL=sua-url \
  -e SUPABASE_KEY=sua-chave \
  -e DATTO_API_KEY=sua-chave-datto \
  -p 5000:5000 \
  nsecops
```

## 📚 Documentação

Toda a documentação está organizada no diretório `docs/`:

- **[📖 Documentação Completa](docs/README.md)** - Guia organizado de toda a documentação
- **[🔧 Configuração EasyPanel](docs/EASYPANEL_ENV_SETUP.md)** - Configuração de variáveis
- **[🚀 API Datto](docs/DATTO_API_SETUP.md)** - Configuração da API Datto RMM
- **[🛠️ Configuração Postman](docs/POSTMAN_SETUP.md)** - Coleção para testar a API Datto
- **[🔐 Google OAuth Setup](docs/GOOGLE_OAUTH_SETUP.md)** - Configuração Google OAuth
- **[📊 Avaliação Sistema](docs/AVALIACAO_SISTEMA.md)** - Avaliação completa
- **[📋 Resumo Implementação](docs/RESUMO_IMPLEMENTACAO.md)** - Resumo da implementação

## 📞 Suporte

Para problemas ou dúvidas:
- Email: resper@ness.com.br
- Repositório: https://github.com/resper1965/ndatto-1
- Documentação: [docs/README.md](docs/README.md)

---

**Desenvolvido por:** Ricardo Esper  
**Empresa:** Ness  
**Versão:** 1.0.0  
**Última Atualização:** Janeiro 2025