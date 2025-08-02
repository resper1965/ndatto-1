# n.secops - Sistema de Monitoramento de Dispositivos

Sistema de monitoramento e gerenciamento de dispositivos baseado em Flask e Supabase.

## 🚀 Configuração Rápida

### 1. Variáveis de Ambiente

#### Para Desenvolvimento Local

Crie um arquivo `.env` na raiz do projeto:

```bash
# Publishable key (safe for browser)
NEXT_PUBLIC_SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX

# Secret key (backend only)
SUPABASE_SERVICE_ROLE_KEY=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW

# Datto RMM API
DATTO_API_KEY=1V90QH7BHSALBD3UVVCDNK4P6EGC9GRH
DATTO_API_SECRET=81RR0IRHJEMSP7QELPC52USS967LBD5F

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
```

#### Para Produção (Docker)

Configure as variáveis de ambiente no seu sistema de deploy:

**EasyPanel:**
- Vá para as configurações do projeto
- Adicione as seguintes variáveis de ambiente:

```bash
SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
SUPABASE_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX
SUPABASE_SECRET=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW
SECRET_KEY=your-production-secret-key-here
FLASK_APP=app.py
FLASK_ENV=production
```

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
| `NEXT_PUBLIC_SUPABASE_URL` | URL do projeto Supabase | `https://pszfqqmmljekibmcgmig.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Chave pública do Supabase | `sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX` |
| `SUPABASE_SERVICE_ROLE_KEY` | Chave secreta do Supabase | `sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW` |
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
ndatto-1/
├── app.py                 # Aplicação principal Flask
├── supabase_client.py     # Cliente Supabase
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
├── .env                  # Variáveis de ambiente (local)
├── .gitignore           # Arquivos ignorados pelo Git
├── static/              # Arquivos estáticos
│   ├── css/
│   └── js/
└── templates/           # Templates HTML
    ├── base.html
    ├── dashboard.html
    ├── login.html
    └── ...
```

## 🔐 Segurança

- **Nunca** commite o arquivo `.env` no Git
- Use chaves diferentes para desenvolvimento e produção
- Configure Row Level Security (RLS) no Supabase
- Use HTTPS em produção
- Troque a `SECRET_KEY` em produção

## 📞 Suporte

Para problemas ou dúvidas:
- Email: resper@ness.com.br
- Repositório: https://github.com/resper1965/ndatto-1

---

**Desenvolvido por:** Ricardo Esper  
**Empresa:** Ness  
**Versão:** 1.0.0