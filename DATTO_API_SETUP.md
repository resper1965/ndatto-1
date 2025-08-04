# Configuração da API Datto RMM

Este documento explica como configurar e usar a API do Datto RMM para coletar dados de dispositivos, sites e alertas.

## 🔑 Obtenção das Chaves da API

### 1. Acesse o Portal Datto RMM

1. Faça login no [Portal Datto RMM](https://centra.centrastage.net)
2. Navegue até **Settings** > **API**
3. Gere uma nova chave de API ou use uma existente

### 2. Configure as Variáveis de Ambiente

#### Para Desenvolvimento Local
Adicione as seguintes variáveis ao seu arquivo `.env`:

```bash
# Datto RMM API
DATTO_API_KEY=sua-chave-api-datto-aqui
DATTO_API_SECRET=seu-segredo-api-datto-aqui
```

#### Para Produção (EasyPanel)
No EasyPanel, configure as variáveis de ambiente:

1. Acesse o painel do EasyPanel
2. Vá para o projeto `nciso-dattormm`
3. Navegue até **Settings** > **Environment Variables**
4. Adicione as variáveis:

```bash
DATTO_API_KEY=sua-chave-real-api-datto
DATTO_API_SECRET=seu-segredo-real-api-datto
```

**Nota:** As variáveis de ambiente no EasyPanel são persistidas automaticamente e ficam disponíveis para a aplicação em produção.

## 🧪 Testando a API

### 1. Teste Básico

Execute o script de teste para verificar a conexão:

```bash
python test_datto_api.py
```

### 2. Teste via Interface Web

1. Acesse a aplicação
2. Faça login
3. Navegue para `/test-collector` para testar o coletor de dados

## 📊 Endpoints da API

### Sites
- **Endpoint**: `/api/v2/sites`
- **Descrição**: Lista todos os sites configurados
- **Dados retornados**: Nome, endereço, status, número de dispositivos

### Dispositivos
- **Endpoint**: `/api/v2/devices`
- **Descrição**: Lista todos os dispositivos monitorados
- **Dados retornados**: Hostname, site, status, IP, último acesso, SO, hardware

### Alertas
- **Endpoint**: `/api/v2/alerts`
- **Descrição**: Lista alertas ativos e recentes
- **Dados retornados**: Tipo, severidade, status, mensagem, dispositivo

### Componentes
- **Endpoint**: `/api/v2/devices/{device_uid}/components`
- **Descrição**: Lista componentes de um dispositivo específico
- **Dados retornados**: CPU, memória, disco, rede, status

## 🔄 Sincronização de Dados

### Sincronização Manual

1. Acesse `/sync` na aplicação
2. O sistema irá:
   - Coletar dados da API do Datto
   - Limpar dados antigos no Supabase
   - Inserir novos dados
   - Atualizar estatísticas

### Sincronização Automática

Para configurar sincronização automática, adicione um cron job:

```bash
# Sincronizar a cada 15 minutos
*/15 * * * * curl -X GET https://seu-dominio.com/sync
```

## 📈 Dados Coletados

### Sites
```json
{
  "uid": "site-001",
  "name": "Matriz - São Paulo",
  "address": "Rua das Flores, 123 - São Paulo/SP",
  "status": "active",
  "device_count": 15,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Dispositivos
```json
{
  "uid": "dev-001",
  "hostname": "server-sp-01",
  "site_uid": "site-001",
  "status": "online",
  "ip_address": "192.168.1.100",
  "last_seen": "2024-01-15T10:30:00Z",
  "os": "Windows Server 2019",
  "memory": "16GB",
  "cpu": "Intel Xeon"
}
```

### Alertas
```json
{
  "uid": "alert-001",
  "device_uid": "dev-003",
  "alert_type": "device_offline",
  "severity": "high",
  "status": "new",
  "message": "Dispositivo server-bh-01 está offline há mais de 30 minutos",
  "created_at": "2024-01-15T09:45:00Z"
}
```

## 🚨 Troubleshooting

### Erro: "Chaves da API não configuradas"

**Solução:**
1. Verifique se as variáveis estão no arquivo `.env`
2. Reinicie a aplicação após adicionar as variáveis
3. Verifique se os nomes das variáveis estão corretos

### Erro: "Erro de autenticação"

**Solução:**
1. Verifique se as chaves da API estão corretas
2. Confirme se a API está ativa no portal Datto
3. Verifique as permissões da chave de API

### Erro: "Acesso negado"

**Solução:**
1. Verifique se a chave de API tem permissões adequadas
2. Confirme se o IP está liberado (se aplicável)
3. Verifique se a conta tem acesso aos dados solicitados

### Dados não aparecem no dashboard

**Solução:**
1. Execute a sincronização manual em `/sync`
2. Verifique os logs da aplicação
3. Teste a API diretamente com `test_datto_api.py`

## 📝 Logs e Debug

### Habilitar Debug

Para desenvolvimento, configure:

```bash
FLASK_ENV=development
```

### Verificar Logs

```bash
# Logs da aplicação
tail -f app.log

# Logs do Docker (se aplicável)
docker logs container-name
```

## 🔧 Configuração Avançada

### Personalizar Endpoints

Edite `data_collector.py` para personalizar os endpoints:

```python
# Exemplo: Adicionar filtros
params = {
    'status': 'online',
    'limit': 100
}
response = await self._make_request("devices", params)
```

### Adicionar Novos Tipos de Dados

1. Crie novo método no `DataCollector`
2. Adicione tabela no Supabase
3. Atualize o `supabase_client.py`
4. Adicione template se necessário

## 📞 Suporte

Para problemas com a API do Datto:
- Documentação oficial: [Datto RMM API](https://developer.datto.com/)
- Suporte técnico: [Datto Support](https://support.datto.com/)

Para problemas com a aplicação:
- Email: resper@ness.com.br
- Repositório: https://github.com/resper1965/ndatto-1 