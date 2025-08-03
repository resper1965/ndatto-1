# Scripts de Deploy Automatizado

## Visão Geral

Este projeto inclui scripts automatizados para fazer deploy da aplicação no EasyPanel.

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

## Como Usar

### Deploy Inteligente (Recomendado)
```bash
./deploy.sh
```

### Deploy Forçado
```bash
./deploy_force.sh
```

## O que os Scripts Fazem

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

## Exemplo de Saída

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

## Configuração

### URL de Deploy
A URL de deploy está configurada nos scripts:
```bash
DEPLOY_URL="http://62.72.8.164:3000/api/deploy/deddad00ec3e4fc63c63f76d2005c2259f9dbd682a9eeb4f"
```

### Permissões
Certifique-se de que os scripts são executáveis:
```bash
chmod +x deploy.sh deploy_force.sh
```

## Troubleshooting

### Erro: "Permission denied"
```bash
chmod +x deploy.sh deploy_force.sh
```

### Erro: "curl: command not found"
Instale o curl:
```bash
sudo apt-get install curl
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

1. **Chamar o script diretamente**:
   ```bash
   ./deploy_force.sh
   ```

2. **Usar apenas a parte de deploy**:
   ```bash
   curl -X POST "http://62.72.8.164:3000/api/deploy/deddad00ec3e4fc63c63f76d2005c2259f9dbd682a9eeb4f"
   ```

3. **Cron job para deploy automático**:
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