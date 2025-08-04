# Configuração do Domínio ndatto.nciso.ness.tec.br

## 🎯 **Configuração no EasyPanel**

### 1. **Configurar Domínio no EasyPanel**

1. Acesse o EasyPanel em `http://62.72.8.164:3000`
2. Vá para o projeto `nciso-dattormm`
3. Na seção **"Domains"** ou **"Custom Domains"**:
   - Adicione: `ndatto.nciso.ness.tec.br`
   - Configure para apontar para a porta `5000`
   - Ative SSL/HTTPS se disponível

### 2. **Configuração de Proxy/Reverse Proxy**

Se necessário, configure o proxy para direcionar:
- `ndatto.nciso.ness.tec.br` → `localhost:5000`

### 3. **Configuração DNS**

Certifique-se de que o DNS aponte para:
- `ndatto.nciso.ness.tec.br` → `62.72.8.164`

## 🔧 **Configurações Aplicadas na Aplicação**

### ✅ **CORS Configurado**
```python
CORS(app, origins=[
    'http://ndatto.nciso.ness.tec.br',
    'https://ndatto.nciso.ness.tec.br',
    'http://localhost:3000',
    'http://localhost:5000'
])
```

### ✅ **Domínios Permitidos**
```python
DOMAIN_CONFIG = {
    'allowed_hosts': [
        'ndatto.nciso.ness.tec.br',
        'localhost',
        '127.0.0.1',
        '62.72.8.164'
    ]
}
```

### ✅ **Middleware de Segurança**
- Verificação automática de domínio
- Bloqueio de domínios não autorizados

## 🚀 **URLs de Acesso**

### **Produção:**
- **Principal**: `https://ndatto.nciso.ness.tec.br`
- **API**: `https://ndatto.nciso.ness.tec.br/api/`
- **Login**: `https://ndatto.nciso.ness.tec.br/login`

### **Desenvolvimento:**
- **Local**: `http://localhost:5000`
- **VPS**: `http://62.72.8.164:3000`

## 📋 **Checklist de Configuração**

- ✅ **DNS**: Configurado para apontar para 62.72.8.164
- ✅ **EasyPanel**: Domínio adicionado
- ✅ **Proxy**: Configurado para porta 5000
- ✅ **SSL**: Ativado (se disponível)
- ✅ **CORS**: Configurado na aplicação
- ✅ **Segurança**: Middleware ativo

## 🎉 **Resultado Final**

Após a configuração, a aplicação estará acessível em:
**`https://ndatto.nciso.ness.tec.br`**

Com todas as funcionalidades:
- ✅ Login seguro
- ✅ Dashboard completo
- ✅ API funcional
- ✅ Monitoramento ativo 