#!/bin/bash

echo "=== Criando todos os arquivos do projeto ==="

# Cria o diretório do projeto se não existir
# mkdir -p /etc/easypanel/projects/nciso/nciso-dattormm/code
# cd /etc/easypanel/projects/nciso/nciso-dattormm/code/

echo "Criando diretórios necessários..."
mkdir -p static/css static/js templates tools

echo "Criando app.py..."
cat > app.py << 'EOF'
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import asyncio
from functools import wraps
from supabase_client import SupabaseManager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# Inicializa o gerenciador do Supabase
supabase = SupabaseManager()

def async_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('access_token')
        if not token:
            return redirect(url_for('login'))
        
        # Verifica se o token ainda é válido
        user = asyncio.run(supabase.verify_token(token))
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
@async_route
async def dashboard():
    # Obtém estatísticas do dashboard
    stats = await supabase.get_dashboard_stats()
    
    # Obtém usuário atual
    user = await supabase.get_user()
    
    return render_template(
        'dashboard.html',
        total_devices=stats['total_devices'],
        online_devices=stats['online_devices'],
        offline_devices=stats['offline_devices'],
        total_alerts=stats['total_alerts'],
        new_alerts=stats['new_alerts'],
        total_sites=stats['total_sites'],
        user=user
    )

@app.route('/login', methods=['GET', 'POST'])
@async_route
async def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('login.html', error="Email e senha são obrigatórios")
        
        # Verifica se o email é do domínio @ness.com.br
        if not email.endswith('@ness.com.br'):
            return render_template('login.html', error="Acesso restrito ao domínio @ness.com.br")
        
        # Tenta fazer login
        result = await supabase.sign_in(email, password)
        
        if 'error' in result:
            return render_template('login.html', error=result['error'])
        
        # Armazena o token na sessão
        session['access_token'] = result['session']['access_token']
        session['refresh_token'] = result['session']['refresh_token']
        session['user'] = result['user']
        
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
@async_route
async def logout():
    await supabase.sign_out()
    session.clear()
    return redirect(url_for('login'))

@app.route('/devices')
@login_required
@async_route
async def devices():
    page = request.args.get('page', 1, type=int)
    site_uid = request.args.get('site_uid', '')
    status = request.args.get('status', '')
    
    filters = {}
    if site_uid:
        filters['site_uid'] = site_uid
    if status:
        filters['status'] = status
    
    devices = await supabase.get_devices(filters)
    
    return render_template(
        'devices.html',
        devices=devices,
        current_page=page,
        site_uid=site_uid,
        status=status
    )

@app.route('/device/<device_uid>')
@login_required
@async_route
async def device_detail(device_uid):
    device = await supabase.get_device_details(device_uid)
    components = await supabase.get_device_components(device_uid) if device else []
    
    return render_template(
        'device_detail.html',
        device=device,
        components=components
    )

@app.route('/alerts')
@login_required
@async_route
async def alerts():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    filters = {}
    if status:
        filters['status'] = status
    
    alerts = await supabase.get_alerts(filters)
    
    return render_template(
        'alerts.html',
        alerts=alerts,
        current_page=page,
        status=status
    )

@app.route('/resolve_alert/<alert_uid>')
@login_required
@async_route
async def resolve_alert_route(alert_uid):
    success = await supabase.resolve_alert(alert_uid)
    
    if success:
        return redirect(url_for('alerts'))
    else:
        return "Erro ao resolver alerta", 500

@app.route('/sites')
@login_required
@async_route
async def sites():
    page = request.args.get('page', 1, type=int)
    sites = await supabase.get_sites()
    
    return render_template(
        'sites.html',
        sites=sites,
        current_page=page
    )

@app.route('/sync')
@login_required
@async_route
async def sync_data():
    """Endpoint para sincronizar dados manualmente."""
    from data_collector import DataCollector
    
    collector = DataCollector()
    await collector.collect_all_data()
    
    return redirect(url_for('dashboard'))

@app.route('/api/user')
@login_required
@async_route
async def get_user():
    """API endpoint para obter informações do usuário."""
    user = await supabase.get_user()
    if user:
        return jsonify({
            'id': user['id'],
            'email': user['email'],
            'created_at': user['created_at']
        })
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
EOF

echo "Criando supabase_client.py..."
cat > supabase_client.py << 'EOF'
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional, Tuple
import asyncio

load_dotenv()

class SupabaseManager:
    def __init__(self):
        self.supabase_url: str = os.getenv("SUPABASE_URL")
        self.supabase_key: str = os.getenv("SUPABASE_KEY")
        self.supabase_secret: str = os.getenv("SUPABASE_SECRET")
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        
    async def sign_up(self, email: str, password: str) -> Dict[str, Any]:
        """Registra um novo usuário."""
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            return response
        except Exception as e:
            print(f"Erro ao registrar usuário: {e}")
            return {"error": str(e)}
    
    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Faz login de um usuário."""
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return {"error": str(e)}
    
    async def sign_out(self) -> bool:
        """Faz logout do usuário."""
        try:
            self.client.auth.sign_out()
            return True
        except Exception as e:
            print(f"Erro ao fazer logout: {e}")
            return False
    
    async def get_user(self) -> Optional[Dict[str, Any]]:
        """Obtém o usuário atual."""
        try:
            user = self.client.auth.get_user()
            return user.user if user else None
        except Exception as e:
            print(f"Erro ao obter usuário: {e}")
            return None
    
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifica se o token JWT é válido."""
        try:
            # Para verificar o token, precisamos criar um cliente com a chave secreta
            admin_client = create_client(self.supabase_url, self.supabase_secret)
            user = admin_client.auth.get_user(token)
            return user.user if user else None
        except Exception as e:
            print(f"Erro ao verificar token: {e}")
            return None
    
    async def get_devices(self, filters: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtém dispositivos com filtros opcionais."""
        try:
            query = self.client.table('devices').select('*').limit(limit)
            
            if filters:
                if 'site_uid' in filters:
                    query = query.eq('site_uid', filters['site_uid'])
                if 'status' in filters and filters['status'] != 'all':
                    query = query.eq('status', filters['status'])
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao obter dispositivos: {e}")
            return []
    
    async def get_device_details(self, device_uid: str) -> Optional[Dict[str, Any]]:
        """Obtém detalhes de um dispositivo específico."""
        try:
            response = self.client.table('devices').select('*').eq('uid', device_uid).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao obter detalhes do dispositivo: {e}")
            return None
    
    async def get_alerts(self, filters: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtém alertas com filtros opcionais."""
        try:
            query = self.client.table('alerts').select('*').limit(limit)
            
            if filters:
                if 'status' in filters and filters['status'] != 'all':
                    query = query.eq('status', filters['status'])
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao obter alertas: {e}")
            return []
    
    async def get_sites(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtém todos os sites."""
        try:
            response = self.client.table('sites').select('*').limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao obter sites: {e}")
            return []
    
    async def get_device_components(self, device_uid: str) -> List[Dict[str, Any]]:
        """Obtém componentes de um dispositivo."""
        try:
            response = self.client.table('device_components').select('*').eq('device_uid', device_uid).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao obter componentes: {e}")
            return []
    
    async def resolve_alert(self, alert_uid: str) -> bool:
        """Marca um alerta como resolvido."""
        try:
            response = self.client.table('alerts').update({'status': 'resolved'}).eq('uid', alert_uid).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Erro ao resolver alerta: {e}")
            return False
    
    async def create_audit_log(self, action: str, entity_type: str, entity_id: str, details: Dict[str, Any]) -> bool:
        """Cria um log de auditoria."""
        try:
            log_data = {
                'action': action,
                'entity_type': entity_type,
                'entity_id': entity_id,
                'details': details
            }
            response = self.client.table('audit_logs').insert(log_data).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Erro ao criar log de auditoria: {e}")
            return False
    
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas para o dashboard."""
        try:
            # Total de dispositivos
            devices_response = self.client.table('devices').select('count', count='exact').execute()
            total_devices = devices_response.count if hasattr(devices_response, 'count') else 0
            
            # Dispositivos online
            online_response = self.client.table('devices').select('count', count='exact').eq('status', 'online').execute()
            online_devices = online_response.count if hasattr(online_response, 'count') else 0
            
            # Dispositivos offline
            offline_devices = total_devices - online_devices
            
            # Total de alertas
            alerts_response = self.client.table('alerts').select('count', count='exact').execute()
            total_alerts = alerts_response.count if hasattr(alerts_response, 'count') else 0
            
            # Alertas novos
            new_alerts_response = self.client.table('alerts').select('count', count='exact').eq('status', 'new').execute()
            new_alerts = new_alerts_response.count if hasattr(new_alerts_response, 'count') else 0
            
            # Total de sites
            sites_response = self.client.table('sites').select('count', count='exact').execute()
            total_sites = sites_response.count if hasattr(sites_response, 'count') else 0
            
            return {
                'total_devices': total_devices,
                'online_devices': online_devices,
                'offline_devices': offline_devices,
                'total_alerts': total_alerts,
                'new_alerts': new_alerts,
                'total_sites': total_sites
            }
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {
                'total_devices': 0,
                'online_devices': 0,
                'offline_devices': 0,
                'total_alerts': 0,
                'new_alerts': 0,
                'total_sites': 0
            }
EOF

echo "Criando Dockerfile..."
cat > Dockerfile << 'EOF'
# Use uma imagem Python oficial como base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Define variáveis de ambiente para evitar que o Python escreva arquivos .pyc e buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo requirements.txt e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY . .

# Cria um usuário não-root para segurança
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expõe a porta que a aplicação Flask irá rodar
EXPOSE 5000

# Comando para executar a aplicação
CMD ["python", "app.py"]
EOF

echo "Criando requirements.txt..."
cat > requirements.txt << 'EOF'
Flask==2.3.3
supabase==2.3.0
httpx==0.25.0
python-dotenv==1.0.0
mcp
EOF

echo "Criando .env..."
cat > .env << 'EOF'
# Datto RMM API
DATTO_API_KEY=1V90QH7BHSALBD3UVVCDNK4P6EGC9GRH
DATTO_API_SECRET=81RR0IRHJEMSP7QELPC52USS967LBD5F

# Supabase
SUPABASE_URL=https://pszfqqmmljekibmcgmig.supabase.co
SUPABASE_KEY=sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX
SUPABASE_SECRET=sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
EOF

echo "Criando templates/base.html..."
mkdir -p templates
cat > templates/base.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>n.secops</title>
    
    <!-- Google Fonts: Montserrat -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    
    <!-- Configuração do Tailwind -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#00ade8',
                        gray: {
                            50: '#0f0f0f',
                            100: '#1a1a1a',
                            200: '#252525',
                            300: '#333333',
                            400: '#404040',
                            500: '#666666',
                            600: '#808080',
                            700: '#a0a0a0',
                            800: '#cccccc',
                            900: '#ffffff',
                        }
                    },
                    fontFamily: {
                        sans: ['Montserrat', 'sans-serif'],
                    },
                }
            }
        }
    </script>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container mx-auto px-4">
            <div class="flex justify-between items-center py-4">
                <a href="{{ url_for('dashboard') }}" class="navbar-brand font-bold text-2xl flex items-center">
                    n<span class="logo-dot">.</span>secops
                </a>
                
                <!-- Mobile menu button -->
                <button class="navbar-toggler lg:hidden" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <i class="bi bi-list text-2xl"></i>
                </button>
                
                <!-- Desktop menu -->
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        {% if session.get('access_token') %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('dashboard') }}">
                                <i class="bi bi-speedometer2 me-2"></i> Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('devices') }}">
                                <i class="bi bi-pc-display me-2"></i> Devices
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('alerts') }}">
                                <i class="bi bi-exclamation-triangle me-2"></i> Alerts
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('sites') }}">
                                <i class="bi bi-building me-2"></i> Sites
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('sync') }}">
                                <i class="bi bi-arrow-clockwise me-2"></i> Sync
                            </a>
                        </li>
                        
                        <!-- User menu -->
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" role="button" data-bs-toggle="dropdown">
                                <div class="h-8 w-8 rounded-full bg-primary d-flex align-items-center justify-center text-white font-medium me-2">
                                    {{ session.get('user', {}).get('email', 'U')[0]|upper }}
                                </div>
                            </a>
                            <ul class="dropdown-menu">
                                <li><span class="dropdown-item-text">{{ session.get('user', {}).get('email', '') }}</span></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="{{ url_for('logout') }}"><i class="bi bi-box-arrow-right me-2"></i> Sair</a></li>
                            </ul>
                        </li>
                        {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('login') }}">Login</a>
                        </li>
                        {% endif %}
                    </ul>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main content -->
    <main class="flex-grow container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="mt-5">
        <div class="container mx-auto px-4">
            <p class="text-center mb-0">
                n<span class="logo-dot">.</span>powered by ness<span class="logo-dot">.</span>
            </p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
EOF

echo "Criando templates/login.html..."
cat > templates/login.html << 'EOF'
{% extends "base.html" %}

{% block content %}
<div class="login-container">
    <div class="login-card">
        <div class="text-center mb-4">
            <a href="#" class="text-gray-900 font-bold text-3xl flex items-center justify-center">
                n<span class="logo-dot">.</span>secops
            </a>
            <h2 class="mt-4">Faça login na sua conta</h2>
            <p class="text-muted">Acesso restrito ao domínio @ness.com.br</p>
        </div>
        
        {% if error %}
        <div class="alert alert-danger" role="alert">
            {{ error }}
        </div>
        {% endif %}
        
        <div class="d-grid gap-3">
            <!-- Formulário de login com email/senha -->
            <form method="POST">
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control login-input" id="email" name="email" required placeholder="Email (@ness.com.br)">
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Senha</label>
                    <input type="password" class="form-control login-input" id="password" name="password" required placeholder="Senha">
                </div>
                <button type="submit" class="btn btn-primary w-100">Entrar</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
EOF

echo "Criando templates/dashboard.html..."
cat > templates/dashboard.html << 'EOF'
{% extends "base.html" %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>Dashboard</h1>
    <div class="d-flex align-items-center">
        <span class="me-2 text-muted">Last updated:</span>
        <span id="last-update" class="fw-medium">Just now</span>
    </div>
</div>

<div class="row mb-4">
    <div class="col-md-3 mb-3">
        <div class="card dashboard-card primary h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h4 class="mb-1">{{ total_devices }}</h4>
                        <p class="mb-0 text-muted">Total Devices</p>
                    </div>
                    <div class="text-primary">
                        <i class="bi bi-pc-display icon-large"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-3 mb-3">
        <div class="card dashboard-card success h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h4 class="mb-1">{{ online_devices }}</h4>
                        <p class="mb-0 text-muted">Online Devices</p>
                    </div>
                    <div class="text-success">
                        <i class="bi bi-check-circle icon-large"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-3 mb-3">
        <div class="card dashboard-card danger h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h4 class="mb-1">{{ offline_devices }}</h4>
                        <p class="mb-0 text-muted">Offline Devices</p>
                    </div>
                    <div class="text-danger">
                        <i class="bi bi-x-circle icon-large"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-3 mb-3">
        <div class="card dashboard-card warning h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h4 class="mb-1">{{ new_alerts }}</h4>
                        <p class="mb-0 text-muted">New Alerts</p>
                    </div>
                    <div class="text-warning">
                        <i class="bi bi-exclamation-triangle icon-large"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6 mb-4">
        <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Recent Devices</h5>
                <a href="{{ url_for('devices') }}" class="btn btn-sm btn-outline-primary">View All</a>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Hostname</th>
                                <th>Site</th>
                                <th>Status</th>
                                <th>Last Seen</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td colspan="4" class="text-center text-muted">No recent devices data</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-6 mb-4">
        <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Recent Alerts</h5>
                <a href="{{ url_for('alerts') }}" class="btn btn-sm btn-outline-primary">View All</a>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Device</th>
                                <th>Type</th>
                                <th>Status</th>
                                <th>Created</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td colspan="4" class="text-center text-muted">No recent alerts data</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

echo "Criando static/css/style.css..."
mkdir -p static/css
cat > static/css/style.css << 'EOF' 
/* Variáveis de cores para tema escuro */
:root {
    --primary-color: #00ade8;
    --bg-primary: #0f0f0f;
    --bg-secondary: #1a1a1a;
    --bg-tertiary: #252525;
    --bg-card: #1e1e1e;
    --text-primary: #ffffff;
    --text-secondary: #b0b0b0;
    --text-muted: #808080;
    --border-color: #333333;
    --hover-bg: #2a2a2a;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    --shadow-color: rgba(0, 0, 0, 0.3);
}

body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Montserrat', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Navbar */
.navbar {
    background-color: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border-color);
    box-shadow: 0 4px 6px -1px var(--shadow-color), 0 2px 4px -1px var(--shadow-color);
    padding: 1rem 0;
}

.navbar-brand {
    font-weight: 700;
    font-size: 1.5rem;
    color: var(--text-primary) !important;
    display: flex;
    align
