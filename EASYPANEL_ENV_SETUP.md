# Configuração de Variáveis de Ambiente no EasyPanel

Este guia explica como configurar as variáveis de ambiente no EasyPanel para o sistema NCISO.

## 🎯 Objetivo

Configurar todas as variáveis necessárias para que o sistema funcione corretamente em produção, incluindo a integração com a API do Datto RMM.

## 📋 Variáveis Obrigatórias

### 1. Acesse o EasyPanel

1. Faça login no [EasyPanel](https://easypanel.io)
2. Navegue até o projeto `nciso-dattormm`
3. Clique em **Settings** no menu lateral
4. Selecione **Environment Variables**

### 2. Configure as Variáveis

Adicione as seguintes variáveis uma por uma:

#### Supabase Configuration
```bash
SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
```

```bash
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzemZxcW1tbGpla2libWNnbWlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE5NDE4NTAsImV4cCI6MjA2NzUxNzg1MH0.y5-XyIFRpBX8uolv6IzvcNHs0_Xm6Q3eV74YFc_Vc6s
```

```bash
SUPABASE_SECRET=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzemZxcW1tbGpla2libWNnbWlnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTk0MTg1MCwiZXhwIjoyMDY3NTE3ODUwfQ.LL99WTJPqiTQNViTduyi8r5itQSkaw1b9Gomv58Ajyk
```

#### Flask Configuration
```bash
FLASK_APP=app.py
```

```bash
FLASK_ENV=production
```

```bash
SECRET_KEY=nciso-prod-2025-secure-key-change-in-production
```

#### Datto RMM API Configuration
```bash
DATTO_API_KEY=sua-chave-real-api-datto
```

```bash
DATTO_API_SECRET=seu-segredo-real-api-datto
```

## 🔧 Como Adicionar Variáveis

### Passo a Passo:

1. **Clique em "Add Variable"**
2. **Nome da Variável**: Digite o nome (ex: `SUPABASE_URL`)
3. **Valor**: Cole o valor correspondente
4. **Tipo**: Selecione "Plain" (padrão)
5. **Clique em "Save"**

### Exemplo:
- **Nome**: `DATTO_API_KEY`
- **Valor**: `1V90QH7BHSALBD3UVVCDNK4P6EGC9GRH`
- **Tipo**: `Plain`

## ✅ Verificação

### 1. Verificar se todas as variáveis estão configuradas:

Você deve ter **8 variáveis** configuradas:

- ✅ `SUPABASE_URL`
- ✅ `SUPABASE_KEY`
- ✅ `SUPABASE_SECRET`
- ✅ `FLASK_APP`
- ✅ `FLASK_ENV`
- ✅ `SECRET_KEY`
- ✅ `DATTO_API_KEY`
- ✅ `DATTO_API_SECRET`

### 2. Reiniciar a aplicação:

Após configurar todas as variáveis:

1. Vá para **Deployments**
2. Clique em **Redeploy** na aplicação
3. Aguarde o deploy completar
4. Verifique os logs para confirmar que não há erros

## 🧪 Teste da Configuração

### 1. Verificar logs da aplicação:

```bash
# No EasyPanel, vá para Logs
# Procure por mensagens como:
# "✅ Conexão com a API estabelecida!"
# "✅ Sites encontrados: X"
# "✅ Dispositivos encontrados: X"
```

### 2. Testar via interface web:

1. Acesse a aplicação
2. Faça login
3. Navegue para `/test-collector`
4. Verifique se retorna dados da API

### 3. Testar sincronização:

1. Acesse `/sync` na aplicação
2. Verifique logs para confirmar coleta
3. Confirme dados no dashboard

## 🚨 Troubleshooting

### Erro: "Chaves da API não configuradas"

**Solução:**
1. Verifique se `DATTO_API_KEY` e `DATTO_API_SECRET` estão configuradas
2. Confirme que os valores estão corretos
3. Reinicie a aplicação após adicionar as variáveis

### Erro: "Erro de autenticação Supabase"

**Solução:**
1. Verifique se `SUPABASE_URL`, `SUPABASE_KEY` e `SUPABASE_SECRET` estão configuradas
2. Confirme que as chaves são válidas
3. Teste a conexão com o Supabase

### Erro: "Aplicação não inicia"

**Solução:**
1. Verifique se `FLASK_APP` e `FLASK_ENV` estão configuradas
2. Confirme se `SECRET_KEY` está definida
3. Verifique logs para erros específicos

## 📝 Notas Importantes

### Segurança:
- ⚠️ **Nunca** commite chaves da API no Git
- ⚠️ Use chaves diferentes para desenvolvimento e produção
- ⚠️ Troque a `SECRET_KEY` em produção
- ⚠️ Monitore logs para detectar tentativas de acesso não autorizado

### Persistência:
- ✅ As variáveis no EasyPanel são persistidas automaticamente
- ✅ Ficam disponíveis para todas as instâncias da aplicação
- ✅ São mantidas entre deploys
- ✅ Podem ser editadas sem reiniciar a aplicação

### Backup:
- 📋 Mantenha um backup das variáveis em local seguro
- 📋 Documente as configurações para referência futura
- 📋 Use um gerenciador de senhas para armazenar chaves

## 🔄 Atualização de Variáveis

### Para atualizar uma variável:

1. Vá para **Settings** > **Environment Variables**
2. Encontre a variável que deseja alterar
3. Clique no ícone de edição
4. Modifique o valor
5. Clique em **Save**
6. **Redeploy** a aplicação

### Para adicionar nova variável:

1. Clique em **Add Variable**
2. Configure nome e valor
3. Clique em **Save**
4. **Redeploy** a aplicação

## 📞 Suporte

Se encontrar problemas:

1. **Verifique logs** da aplicação no EasyPanel
2. **Teste conectividade** com `python test_datto_api.py`
3. **Confirme variáveis** estão configuradas corretamente
4. **Contate suporte** se necessário

---

**Última Atualização**: Janeiro 2025  
**Versão**: 1.0.0 