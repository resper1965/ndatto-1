# Comandos para Verificar a VPS

## 1. Conectar via SSH
```bash
ssh root@62.72.8.164
```

## 2. Navegar para o diretório da aplicação
```bash
cd /etc/easypanel/projects/nciso/nciso-dattormm/code
```

## 3. Verificar variáveis de ambiente
```bash
env | grep SUPABASE
```

## 4. Verificar containers Docker
```bash
docker ps
```

## 5. Verificar logs da aplicação
```bash
# Se o container se chama "dattormm"
docker logs dattormm --tail 20

# Ou ver todos os containers
docker ps -a
```

## 6. Verificar arquivos da aplicação
```bash
ls -la
```

## 7. Verificar se há arquivo .env
```bash
ls -la .env
```

## 8. Verificar logs do EasyPanel
```bash
# Ver logs do sistema
journalctl -u easypanel --tail 20

# Ou ver logs do Docker
docker logs $(docker ps -q --filter 'name=dattormm') --tail 20
```

## 9. Reiniciar aplicação (se necessário)
```bash
# Via EasyPanel (recomendado)
# Ou via Docker
docker restart dattormm
```

## 10. Verificar variáveis no EasyPanel
```bash
# Verificar se as variáveis estão configuradas no EasyPanel
# Acesse o painel do EasyPanel e verifique as variáveis de ambiente
```

## Comandos Rápidos (copie e cole)

### Verificar tudo de uma vez:
```bash
ssh root@62.72.8.164 << 'EOF'
cd /etc/easypanel/projects/nciso/nciso-dattormm/code
echo "=== VARIÁVEIS DE AMBIENTE ==="
env | grep SUPABASE
echo ""
echo "=== CONTAINERS DOCKER ==="
docker ps
echo ""
echo "=== LOGS DA APLICAÇÃO ==="
docker logs $(docker ps -q --filter 'name=dattormm') --tail 10
echo ""
echo "=== ARQUIVOS DA APLICAÇÃO ==="
ls -la
EOF
```

## O que procurar:

### ✅ Variáveis corretas:
```
SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
SUPABASE_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX
SUPABASE_SECRET=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW
```

### ❌ Variáveis incorretas:
```
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Próximos passos:

1. **Execute os comandos** acima na VPS
2. **Verifique as variáveis** - devem ser SUPABASE_* não NEXT_PUBLIC_*
3. **Configure no EasyPanel** se necessário
4. **Reinicie a aplicação** se houver mudanças 