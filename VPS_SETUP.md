# Configuração da VPS - EasyPanel

## Problema Identificado

A aplicação na VPS não está carregando as variáveis de ambiente corretamente. Os logs mostram:
```
SUPABASE_KEY: None
SUPABASE_SECRET: None
```

## Solução: Configurar Variáveis no EasyPanel

### 1. Acesse o EasyPanel
- Faça login no painel do EasyPanel
- Vá para o projeto da sua aplicação

### 2. Configure as Variáveis de Ambiente
Na seção de configurações do projeto, adicione **EXATAMENTE** estas variáveis:

```bash
SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
SUPABASE_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX
SUPABASE_SECRET=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW
SECRET_KEY=sua-chave-secreta-de-producao-aqui
FLASK_APP=app.py
FLASK_ENV=production
```

### 3. Variáveis Opcionais (se necessário)
```bash
DATTO_API_KEY=1V90QH7BHSALBD3UVVCDNK4P6EGC9GRH
DATTO_API_SECRET=81RR0IRHJEMSP7QELPC52USS967LBD5F
```

### 4. Importante: Nomes Corretos
**❌ NÃO USE** estes nomes (antigos):
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
```

**✅ USE** estes nomes (corretos):
```
SUPABASE_URL
SUPABASE_KEY
SUPABASE_SECRET
```

## Verificação

### 1. Após configurar as variáveis:
1. **Reinicie a aplicação** no EasyPanel
2. **Verifique os logs** da aplicação
3. **Teste a aplicação** no navegador

### 2. Logs esperados:
```
=== DEBUG APP.PY ===
SUPABASE_URL: https://pszfqqmmljekibmcgmig.supabase.co
SUPABASE_KEY: sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX
SUPABASE_SECRET: sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW
SECRET_KEY: sua-chave-secreta-de-producao-aqui
===================
```

### 3. Se ainda houver problemas:
- Verifique se não há espaços extras nas variáveis
- Confirme se os valores estão corretos
- Reinicie a aplicação novamente

## Deploy Automático

O deploy automático já está configurado. Após configurar as variáveis:

1. **Faça um commit** (qualquer mudança)
2. **O deploy acontecerá automaticamente**
3. **Verifique os logs** para confirmar

## Troubleshooting

### Erro: "Invalid API key"
- Verifique se `SUPABASE_SECRET` está correto
- Confirme se não há espaços extras
- Verifique se o projeto Supabase está ativo

### Erro: "SUPABASE_KEY: None"
- Verifique se `SUPABASE_KEY` está configurada no EasyPanel
- Confirme se o nome da variável está exato
- Reinicie a aplicação

### Erro: "SUPABASE_SECRET: None"
- Verifique se `SUPABASE_SECRET` está configurada no EasyPanel
- Confirme se o nome da variável está exato
- Reinicie a aplicação

## Comandos Úteis

### Para verificar variáveis na VPS:
```bash
# Acesse a VPS via SSH
ssh usuario@ip-da-vps

# Verifique as variáveis de ambiente
env | grep SUPABASE
```

### Para reiniciar aplicação:
```bash
# No EasyPanel, reinicie a aplicação
# Ou via SSH:
docker restart nome-do-container
```

## Resumo

1. **Configure as variáveis no EasyPanel** com os nomes corretos
2. **Reinicie a aplicação**
3. **Verifique os logs**
4. **Teste a aplicação**

As variáveis devem ser configuradas no **EasyPanel**, não no código local. 