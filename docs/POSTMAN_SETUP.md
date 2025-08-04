# 🚀 Configuração do Postman para Datto API

## 📋 **Passo a Passo**

### 1. **Importar a Coleção**
1. Abra o Postman
2. Clique em "Import"
3. Selecione o arquivo `postman_collection.json`
4. A coleção "Datto RMM API" será criada

### 2. **Configurar Variáveis de Ambiente**

#### **Criar Novo Environment:**
1. Clique no ícone de engrenagem (⚙️) no canto superior direito
2. Clique em "Add"
3. Nome: `Datto API - Development`

#### **Adicionar Variáveis:**
```
DATTO_API_KEY = sua_api_key_aqui
DATTO_API_SECRET = seu_api_secret_aqui
device_uid = uid_do_dispositivo_para_testar
```

### 3. **Testar Conexão**

#### **Primeiro Teste - Sites:**
1. Selecione o environment "Datto API - Development"
2. Vá para `Authentication > Test API Connection`
3. Clique em "Send"
4. **Status esperado:** 200 OK
5. **Response esperado:** Lista de sites ou erro de autenticação

### 4. **Estrutura da Coleção**

#### **📁 Authentication**
- `Test API Connection` - Testa se as credenciais estão funcionando

#### **📁 Sites**
- `Get All Sites` - Lista todos os sites

#### **📁 Devices**
- `Get All Devices` - Lista todos os dispositivos
- `Get Device Components` - Componentes de um dispositivo específico

#### **📁 Alerts**
- `Get All Alerts` - Lista todos os alertas

## 🔧 **Configuração para Desenvolvimento**

### **Headers Padrão:**
```
X-API-Key: {{api_key}}
X-API-Secret: {{api_secret}}
Content-Type: application/json
```

### **URL Base:**
```
https://centraapi.centrastage.net/api/v2
```

## 🧪 **Testes Recomendados**

### **1. Teste de Autenticação**
```bash
GET {{base_url}}/sites
Headers: X-API-Key, X-API-Secret
```

### **2. Teste de Sites**
```bash
GET {{base_url}}/sites
```

### **3. Teste de Devices**
```bash
GET {{base_url}}/devices
```

### **4. Teste de Alerts**
```bash
GET {{base_url}}/alerts
```

### **5. Teste de Components**
```bash
GET {{base_url}}/devices/{{device_uid}}/components
```

## 📊 **Respostas Esperadas**

### **Sites (200 OK):**
```json
{
  "sites": [
    {
      "uid": "site_uid",
      "name": "Site Name",
      "description": "Site Description"
    }
  ]
}
```

### **Devices (200 OK):**
```json
{
  "devices": [
    {
      "uid": "device_uid",
      "name": "Device Name",
      "siteUid": "site_uid",
      "status": "online"
    }
  ]
}
```

### **Alerts (200 OK):**
```json
{
  "alerts": [
    {
      "uid": "alert_uid",
      "deviceUid": "device_uid",
      "message": "Alert message",
      "severity": "warning"
    }
  ]
}
```

## ⚠️ **Possíveis Erros**

### **401 Unauthorized:**
- Verificar se `DATTO_API_KEY` e `DATTO_API_SECRET` estão corretos
- Verificar se as credenciais têm permissão para a API

### **403 Forbidden:**
- Verificar se o IP está na whitelist da Datto
- Verificar se a conta tem acesso aos endpoints

### **404 Not Found:**
- Verificar se a URL base está correta
- Verificar se o endpoint existe

## 🎯 **Próximos Passos**

1. **Teste todos os endpoints** para verificar se funcionam
2. **Salve as respostas** como exemplos para o desenvolvimento
3. **Configure variáveis** para diferentes ambientes (dev/prod)
4. **Crie testes automatizados** para validar as respostas

## 📝 **Notas Importantes**

- **Mantenha as credenciais seguras** - não compartilhe o environment
- **Use diferentes environments** para dev/prod
- **Documente as respostas** para referência futura
- **Teste regularmente** para garantir que a API está funcionando

---

**🎉 Agora você tem uma coleção completa para testar a Datto API!** 