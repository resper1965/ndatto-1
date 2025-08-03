# Conexão SSH com a VPS

## Informações Necessárias

Para conectar via SSH, você precisa das seguintes informações:

### 1. IP da VPS
- Endereço IP da sua VPS
- Exemplo: `62.72.8.164`

### 2. Usuário
- Nome do usuário na VPS
- Exemplo: `root`, `ubuntu`, `admin`, etc.

### 3. Método de Autenticação
- **Chave SSH** (recomendado)
- **Senha** (menos seguro)

## Métodos de Conexão

### Método 1: Usando Chave SSH (Recomendado)

#### 1.1 Gerar Chave SSH (se não tiver)
```bash
# Gerar nova chave SSH
ssh-keygen -t rsa -b 4096 -C "seu-email@exemplo.com"

# A chave será salva em:
# ~/.ssh/id_rsa (chave privada)
# ~/.ssh/id_rsa.pub (chave pública)
```

#### 1.2 Copiar Chave para VPS
```bash
# Copiar chave pública para VPS
ssh-copy-id usuario@ip-da-vps

# Ou manualmente:
cat ~/.ssh/id_rsa.pub | ssh usuario@ip-da-vps "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

#### 1.3 Conectar
```bash
# Conexão básica
ssh usuario@ip-da-vps

# Com porta específica (se necessário)
ssh -p 22 usuario@ip-da-vps

# Com arquivo de chave específico
ssh -i ~/.ssh/id_rsa usuario@ip-da-vps
```

### Método 2: Usando Senha

```bash
# Conectar com senha
ssh usuario@ip-da-vps

# O sistema pedirá a senha
```

## Exemplos Práticos

### Exemplo 1: Conexão Básica
```bash
ssh root@62.72.8.164
```

### Exemplo 2: Com Chave Específica
```bash
ssh -i ~/.ssh/minha_chave root@62.72.8.164
```

### Exemplo 3: Com Porta Específica
```bash
ssh -p 2222 root@62.72.8.164
```

## Verificação de Conexão

### 1. Testar Conexão
```bash
# Testar se a VPS está acessível
ping 62.72.8.164

# Testar porta SSH
telnet 62.72.8.164 22
```

### 2. Verificar Configuração SSH
```bash
# Verificar configuração SSH local
ssh -T usuario@ip-da-vps

# Se funcionar, você verá uma mensagem de boas-vindas
```

## Comandos Úteis na VPS

### 1. Verificar Variáveis de Ambiente
```bash
# Ver todas as variáveis
env

# Ver apenas variáveis do Supabase
env | grep SUPABASE

# Ver variáveis específicas
echo $SUPABASE_URL
echo $SUPABASE_KEY
echo $SUPABASE_SECRET
```

### 2. Verificar Logs da Aplicação
```bash
# Ver logs do Docker
docker logs nome-do-container

# Ver logs em tempo real
docker logs -f nome-do-container

# Ver logs do sistema
journalctl -u nome-do-servico
```

### 3. Reiniciar Aplicação
```bash
# Reiniciar container
docker restart nome-do-container

# Reiniciar serviço
sudo systemctl restart nome-do-servico
```

## Troubleshooting

### Erro: "Connection refused"
- Verifique se o IP está correto
- Confirme se a porta SSH está aberta
- Verifique se o serviço SSH está rodando na VPS

### Erro: "Permission denied"
- Verifique se o usuário está correto
- Confirme se a senha/chave está correta
- Verifique permissões do arquivo de chave

### Erro: "Host key verification failed"
```bash
# Remover chave antiga
ssh-keygen -R ip-da-vps

# Ou adicionar ao known_hosts
ssh-keyscan -H ip-da-vps >> ~/.ssh/known_hosts
```

## Configuração SSH Avançada

### 1. Arquivo de Configuração SSH
Crie/edite `~/.ssh/config`:
```
Host vps-producao
    HostName 62.72.8.164
    User root
    Port 22
    IdentityFile ~/.ssh/id_rsa
```

### 2. Conectar com Alias
```bash
# Agora você pode conectar apenas com:
ssh vps-producao
```

## Segurança

### 1. Desabilitar Login com Senha
Na VPS, edite `/etc/ssh/sshd_config`:
```
PasswordAuthentication no
```

### 2. Mudar Porta SSH
```
Port 2222
```

### 3. Restringir Usuários
```
AllowUsers root
```

## Resumo Rápido

```bash
# 1. Conectar
ssh root@62.72.8.164

# 2. Verificar variáveis
env | grep SUPABASE

# 3. Ver logs
docker logs nome-do-container

# 4. Reiniciar se necessário
docker restart nome-do-container
```

## Próximos Passos

1. **Conecte via SSH** usando um dos métodos acima
2. **Verifique as variáveis de ambiente** na VPS
3. **Configure as variáveis no EasyPanel** se necessário
4. **Reinicie a aplicação** se houver mudanças 