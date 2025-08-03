# Scripts de Deploy Automatizado

## Visão Geral

Este projeto inclui scripts automatizados para fazer deploy da aplicação no EasyPanel, incluindo **deploy automático via Git hooks**.

## Scripts Disponíveis

### 1. `deploy.sh` - Deploy Inteligente
- **Função**: Verifica se há mudanças no Dockerfile antes de fazer deploy
- **Uso**: `./deploy.sh`
- **Comportamento**: 
  - Só faz deploy se detectar mudanças no Dockerfile
  - Evita deploys desnecessários
  - Ideal para uso em desenvolvimento

### 2. `deploy_force.sh` - Deploy Forçado
- **Função**: Sempre faz deploy, mesmo sem mudanças
- **Uso**: `./deploy_force.sh`
- **Comportamento**:
  - Força deploy sempre
  - Cria commit vazio se não há mudanças
  - Ideal para produção ou quando quer garantir deploy

### 3. `setup_auto_deploy.sh` - Configurar Deploy Automático ⭐
- **Função**: Configura deploy automático via Git hooks
- **Uso**: `./setup_auto_deploy.sh`
- **Comportamento**:
  - Cria hook post-commit
  - Deploy automático após cada commit no branch main
  - Ideal para desenvolvimento contínuo

### 4. `disable_auto_deploy.sh` - Desabilitar Deploy Automático
- **Função**: Remove o hook de deploy automático
- **Uso**: `./disable_auto_deploy.sh`
- **Comportamento**:
  - Remove hook post-commit
  - Faz backup antes de remover
  - Permite reabilitar depois

## Deploy Automático via Git Hooks ⭐

### Como Funciona
O deploy automático é ativado através de um **Git hook post-commit** que:
1. **Executa automaticamente** após cada commit
2. **Só funciona no branch main**
3. **Faz push** para o repositório remoto
4. **Chama a URL de deploy** automaticamente

### Configuração
```bash
# Ativar deploy automático
./setup_auto_deploy.sh

# Desabilitar deploy automático
./disable_auto_deploy.sh
```

### Exemplo de Uso
```bash
# 1. Configurar deploy automático
./setup_auto_deploy.sh

# 2. Fazer commit normalmente
git add .
git commit -m "feat: nova funcionalidade"

# 3. Deploy acontece automaticamente!
# === HOOK POST-COMMIT: DEPLOY AUTOMÁTICO ===
# ✅ Branch main detectado. Iniciando deploy automático...
# 🚀 Fazendo push para o repositório...
# 🌐 Chamando URL de deploy...
# ✅ Deploy automático iniciado com sucesso!
```

## Como Usar

### Deploy Manual
```bash
# Deploy inteligente (só se houver mudanças)
./deploy.sh

# Deploy forçado (sempre)
./deploy_force.sh
```

### Deploy Automático
```bash
# Configurar deploy automático
./setup_auto_deploy.sh

# Fazer commits normalmente - deploy acontece automaticamente!
git add .
git commit -m "sua mensagem"
```

## O que os Scripts Fazem

### Scripts Manuais
1. **Verificação de Mudanças** (apenas `deploy.sh`)
   - Verifica se o Dockerfile foi modificado
   - Sai sem fazer nada se não há mudanças

2. **Git Operations**
   - Adiciona Dockerfile ao git: `git add Dockerfile`
   - Faz commit com timestamp: `git commit -m "deploy: ..."`
   - Faz push para o repositório: `git push`

3. **Deploy Automático**
   - Chama a URL de deploy: `http://62.72.8.164:3000/api/deploy/deddad00ec3e4fc63c63f76d2005c2259f9dbd682a9eeb4f`
   - Verifica resposta HTTP
   - Tenta novamente em caso de erro (apenas `deploy_force.sh`)

### Deploy Automático (Git Hook)
1. **Verificação de Branch**
   - Só executa no branch main
   - Pula deploy em outros branches

2. **Git Operations**
   - Faz push para o repositório: `git push`

3. **Deploy Automático**
   - Chama a URL de deploy
   - Verifica resposta HTTP
   - Mostra logs detalhados

## Exemplo de Saída

### Deploy Manual
```
=== DEPLOY FORÇADO ===
Data/Hora: Sun Aug  3 15:12:19 -03 2025
======================
📦 Adicionando Dockerfile ao git...
💾 Fazendo commit...
🚀 Fazendo push para o repositório...
🌐 Chamando URL de deploy...
📡 Resposta do deploy:
Código HTTP: 200
Resposta: Deploying...
✅ Deploy iniciado com sucesso!
=== DEPLOY CONCLUÍDO ===
```

### Deploy Automático (Git Hook)
```
=== HOOK POST-COMMIT: DEPLOY AUTOMÁTICO ===
Data/Hora: Sun Aug  3 15:14:24 -03 2025
==========================================
✅ Branch main detectado. Iniciando deploy automático...
🚀 Fazendo push para o repositório...
🌐 Chamando URL de deploy...
📡 Resposta do deploy:
Código HTTP: 200
Resposta: Deploying...
✅ Deploy automático iniciado com sucesso!
=== HOOK POST-COMMIT CONCLUÍDO ===
```

## Configuração

### URL de Deploy
A URL de deploy está configurada nos scripts:
```bash
DEPLOY_URL="http://62.72.8.164:3000/api/deploy/deddad00ec3e4fc63c63f76d2005c2259f9dbd682a9eeb4f"
```

### Permissões
Certifique-se de que os scripts são executáveis:
```bash
chmod +x deploy.sh deploy_force.sh setup_auto_deploy.sh disable_auto_deploy.sh
```

## Troubleshooting

### Erro: "Permission denied"
```bash
chmod +x deploy.sh deploy_force.sh setup_auto_deploy.sh disable_auto_deploy.sh
```

### Erro: "curl: command not found"
Instale o curl:
```bash
sudo apt-get install curl
```

### Deploy automático não funciona
```bash
# Verificar se o hook existe
ls -la .git/hooks/post-commit

# Reconfigurar se necessário
./setup_auto_deploy.sh
```

### Erro de Deploy (HTTP 500, 404, etc.)
- Verifique se a URL de deploy está correta
- Confirme se o EasyPanel está funcionando
- Verifique os logs do EasyPanel

### Erro de Git
- Verifique se está no diretório correto
- Confirme se o repositório está configurado
- Verifique se tem permissões de push

## Integração com CI/CD

Para integrar com sistemas de CI/CD, você pode:

1. **Usar deploy automático (Recomendado)**:
   ```bash
   ./setup_auto_deploy.sh
   # Agora cada commit fará deploy automaticamente
   ```

2. **Chamar o script diretamente**:
   ```bash
   ./deploy_force.sh
   ```

3. **Usar apenas a parte de deploy**:
   ```bash
   curl -X POST "http://62.72.8.164:3000/api/deploy/deddad00ec3e4fc63c63f76d2005c2259f9dbd682a9eeb4f"
   ```

4. **Cron job para deploy automático**:
   ```bash
   # Adicionar ao crontab
   0 */6 * * * cd /path/to/project && ./deploy_force.sh
   ```

## Logs e Monitoramento

Os scripts geram logs detalhados que incluem:
- Timestamp de início e fim
- Status de cada etapa
- Código HTTP da resposta
- Mensagens de erro detalhadas

Para monitorar deploys, verifique:
- Logs do script
- Logs do EasyPanel
- Status do repositório Git
- Logs do hook post-commit

## Fluxo de Trabalho Recomendado

### Para Desenvolvimento
1. **Configurar deploy automático**:
   ```bash
   ./setup_auto_deploy.sh
   ```

2. **Trabalhar normalmente**:
   ```bash
   git add .
   git commit -m "sua mudança"
   # Deploy acontece automaticamente!
   ```

### Para Produção
1. **Usar deploy manual quando necessário**:
   ```bash
   ./deploy_force.sh
   ```

2. **Ou manter deploy automático**:
   ```bash
   # Já configurado com setup_auto_deploy.sh
   # Cada commit fará deploy automaticamente
   ``` 