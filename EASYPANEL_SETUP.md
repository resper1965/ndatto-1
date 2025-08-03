# Configuração do EasyPanel

## Variáveis de Ambiente no EasyPanel

Para que a aplicação funcione corretamente no EasyPanel, configure as seguintes variáveis de ambiente:

### 1. Acesse o EasyPanel
- Faça login no painel do EasyPanel
- Vá para o projeto da sua aplicação

### 2. Configure as Variáveis de Ambiente
Na seção de configurações do projeto, adicione as seguintes variáveis:

```bash
SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
SUPABASE_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX
SUPABASE_SECRET=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW
SECRET_KEY=sua-chave-secreta-de-producao-aqui
FLASK_APP=app.py
FLASK_ENV=production
```

### 3. Variáveis Opcionais
Se você estiver usando a API Datto RMM, adicione também:

```bash
DATTO_API_KEY=sua-chave-api-datto
DATTO_API_SECRET=seu-segredo-api-datto
```

### 4. Verificação
Após configurar as variáveis:

1. **Reinicie a aplicação** no EasyPanel
2. **Verifique os logs** para confirmar que as variáveis estão sendo carregadas
3. **Teste a aplicação** para garantir que está funcionando

### 5. Debug
Se houver problemas, verifique os logs da aplicação. Você deve ver algo como:

```
=== DEBUG APP.PY ===
SUPABASE_URL: https://pszfqqmmljekibmcgmig.supabase.co
SUPABASE_KEY: sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX
SUPABASE_SECRET: sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW
SECRET_KEY: sua-chave-secreta-de-producao-aqui
===================
```

### 6. Problemas Comuns

#### Variáveis não estão sendo carregadas
- Verifique se os nomes das variáveis estão exatamente como mostrado acima
- Certifique-se de que não há espaços extras
- Reinicie a aplicação após adicionar as variáveis

#### Erro de conexão com Supabase
- Verifique se as chaves do Supabase estão corretas
- Confirme se a URL do Supabase está correta
- Verifique se o projeto Supabase está ativo

#### Erro de autenticação
- Verifique se o `SECRET_KEY` está definido
- Certifique-se de que está usando uma chave secreta forte em produção

### 7. Teste Local
Para testar localmente com as mesmas variáveis:

```bash
# Execute o script de teste
python test_env.py

# Ou execute a aplicação
python app.py
```

### 8. Logs de Debug
A aplicação agora inclui logs de debug que mostram:
- Quais variáveis estão sendo carregadas
- Se há problemas com a conexão do Supabase
- Status das variáveis de ambiente

Se você vir `❌ NÃO DEFINIDA` para alguma variável, verifique a configuração no EasyPanel. 