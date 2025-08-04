# 🔐 Configuração Google OAuth no Supabase

## 📋 **URLs de Redirecionamento**

Para configurar o Google OAuth no Supabase Dashboard, use estas URLs:

### **Produção:**
```
https://ndatto.ncsio.ness.tec.br/auth/callback
```

### **Desenvolvimento:**
```
http://localhost:5000/auth/callback
```

## 🛠️ **Configuração no Supabase Dashboard**

### **1. Acesse o Dashboard:**
- Vá para [supabase.com](https://supabase.com)
- Acesse seu projeto NCISO
- Navegue para **Authentication** → **Providers**

### **2. Configure o Google Provider:**
- Clique em **Google**
- Ative o toggle **Enable**
- Preencha:
  - **Client ID:** (do Google Cloud Console)
  - **Client Secret:** (do Google Cloud Console)

### **3. URLs de Redirecionamento:**
Adicione estas URLs no campo **Redirect URLs:**
```
https://ndatto.ncsio.ness.tec.br/auth/callback
http://localhost:5000/auth/callback
```

## 🔧 **Configuração no Google Cloud Console**

### **1. Criar Projeto:**
- Acesse [console.cloud.google.com](https://console.cloud.google.com)
- Crie um novo projeto ou use existente

### **2. Ativar Google+ API:**
- Vá para **APIs & Services** → **Library**
- Procure por **Google+ API**
- Clique em **Enable**

### **3. Criar Credenciais:**
- Vá para **APIs & Services** → **Credentials**
- Clique em **Create Credentials** → **OAuth 2.0 Client IDs**
- Tipo: **Web application**
- Nome: **NCISO Google OAuth**

### **4. URLs Autorizadas:**
Adicione estas URLs:
```
https://ndatto.ncsio.ness.tec.br
http://localhost:5000
```

### **5. URLs de Redirecionamento:**
Adicione estas URLs:
```
https://ndatto.ncsio.ness.tec.br/auth/callback
http://localhost:5000/auth/callback
```

## 📝 **Variáveis de Ambiente**

### **EasyPanel (Produção):**
```bash
BASE_URL=https://ndatto.ncsio.ness.tec.br
```

### **Desenvolvimento Local:**
```bash
BASE_URL=http://localhost:5000
```

## 🧪 **Teste da Configuração**

### **1. Teste Local:**
```bash
# Execute a aplicação
python app.py

# Acesse
http://localhost:5000/login

# Clique em "Entrar com Google"
```

### **2. Teste Produção:**
```bash
# Acesse
https://ndatto.ncsio.ness.tec.br/login

# Clique em "Entrar com Google"
```

## ⚠️ **Troubleshooting**

### **Erro: "redirect_uri_mismatch"**
- Verifique se as URLs estão corretas no Google Cloud Console
- Certifique-se de que `https://ndatto.ncsio.ness.tec.br/auth/callback` está listada

### **Erro: "Invalid client"**
- Verifique se o Client ID e Secret estão corretos no Supabase
- Confirme se as credenciais são do projeto correto

### **Erro: "Domain not allowed"**
- Verifique se o domínio está na lista de hosts permitidos
- Confirme se o CORS está configurado corretamente

## 📊 **Logs de Debug**

A aplicação gera logs detalhados para debug:

```bash
# Logs de início do OAuth
🔗 Redirecionando para: https://accounts.google.com/oauth/...

# Logs de callback
🔄 Callback OAuth - Code: abc123..., State: xyz789...

# Logs de sucesso
✅ OAuth bem-sucedido com session
✅ Sessão OAuth configurada com sucesso
```

## 🎯 **Fluxo Completo**

1. **Usuário clica** em "Entrar com Google"
2. **Aplicação redireciona** para `/auth/google`
3. **Supabase gera** URL de autorização Google
4. **Usuário autoriza** no Google
5. **Google redireciona** para `/auth/callback`
6. **Aplicação processa** tokens e cria sessão
7. **Usuário é redirecionado** para dashboard

---

**✅ Configuração completa para domínio: `ndatto.ncsio.ness.tec.br`** 