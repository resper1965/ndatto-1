from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import os
import asyncio
from functools import wraps
from supabase_client import SupabaseManager
from dotenv import load_dotenv

load_dotenv()

# Debug apenas em desenvolvimento
if os.getenv("FLASK_ENV") == "development":
    print("=== DEBUG APP.PY ===")
    print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
    print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))
    print("SUPABASE_SECRET:", os.getenv("SUPABASE_SECRET"))
    print("SECRET_KEY:", os.getenv("SECRET_KEY"))
    print("===================")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# Configurações de produção
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Configuração CORS para domínio personalizado
CORS(app, origins=[
    'http://ndatto.nciso.ness.tec.br',
    'https://ndatto.nciso.ness.tec.br',
    'http://localhost:3000',
    'http://localhost:5000'
])

# Configuração de domínio personalizado
DOMAIN_CONFIG = {
    'allowed_hosts': [
        'ndatto.nciso.ness.tec.br',
        'localhost',
        '127.0.0.1',
        '62.72.8.164'
    ]
}

# Inicializa o gerenciador do Supabase
supabase = SupabaseManager()

# Middleware para verificar domínio (comentado temporariamente)
# @app.before_request
# def check_domain():
#     if request.host not in DOMAIN_CONFIG['allowed_hosts']:
#         return jsonify({'error': 'Domain not allowed'}), 403

def async_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = session.get('access_token')
            print(f"🔍 Verificando token: {'Presente' if token else 'Ausente'}")
            
            if not token:
                print("❌ Token não encontrado na sessão")
                return redirect(url_for('login'))
            
            # Verifica se o token ainda é válido
            print("🔍 Verificando validade do token...")
            user = asyncio.run(supabase.verify_token(token))
            if not user:
                print("❌ Token inválido ou expirado")
                session.clear()
                return redirect(url_for('login'))
            
            print("✅ Token válido - acessando rota")
            return f(*args, **kwargs)
        except Exception as e:
            print(f"❌ Erro no login_required: {e}")
            session.clear()
            return redirect(url_for('login'))
    return decorated_function

@app.route('/')
@login_required
@async_route
async def dashboard():
    try:
        # Obtém estatísticas do dashboard
        stats = await supabase.get_dashboard_stats()
        
        # Obtém dados recentes
        recent_devices = await supabase.get_recent_devices(5)
        recent_alerts = await supabase.get_recent_alerts(5)
        
        # Obtém usuário atual
        user = await supabase.get_user()
        
        return render_template(
            'dashboard.html',
            total_devices=stats.get('total_devices', 0),
            online_devices=stats.get('online_devices', 0),
            offline_devices=stats.get('offline_devices', 0),
            total_alerts=stats.get('total_alerts', 0),
            new_alerts=stats.get('new_alerts', 0),
            total_sites=stats.get('total_sites', 0),
            recent_devices=recent_devices,
            recent_alerts=recent_alerts,
            user=user or {}
        )
    except Exception as e:
        # Em caso de erro, retorna dashboard com dados vazios
        print(f"Erro no dashboard: {e}")
        return render_template(
            'dashboard.html',
            total_devices=0,
            online_devices=0,
            offline_devices=0,
            total_alerts=0,
            new_alerts=0,
            total_sites=0,
            recent_devices=[],
            recent_alerts=[],
            user={}
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
        print(f"🔍 Tentando login para: {email}")
        result = await supabase.sign_in(email, password)
        print(f"📊 Resultado do login: {type(result)}")
        
        # Verifica se houve erro
        if hasattr(result, 'error') and result.error:
            print(f"❌ Erro no login: {result.error}")
            return render_template('login.html', error=str(result.error))
        
        # Verifica se é um dicionário com erro
        if isinstance(result, dict) and 'error' in result:
            print(f"❌ Erro no login (dict): {result['error']}")
            return render_template('login.html', error=result['error'])
        
        # Armazena o token na sessão
        if hasattr(result, 'session') and result.session:
            print("✅ Login bem-sucedido - armazenando tokens")
            session['access_token'] = result.session.access_token
            session['refresh_token'] = result.session.refresh_token
            # Converte o objeto User para dicionário para serialização
            if hasattr(result, 'user') and result.user:
                session['user'] = {
                    'id': result.user.id,
                    'email': result.user.email,
                    'created_at': result.user.created_at.isoformat() if result.user.created_at else None
                }
                print(f"✅ Usuário armazenado: {result.user.email}")
            else:
                session['user'] = {}
                print("⚠️  Usuário não encontrado no resultado")
        elif isinstance(result, dict):
            # Fallback para formato de dicionário
            print("✅ Login bem-sucedido (formato dict)")
            session['access_token'] = result.get('session', {}).get('access_token')
            session['refresh_token'] = result.get('session', {}).get('refresh_token')
            session['user'] = result.get('user', {})
        else:
            # Se não conseguiu fazer login, retorna erro
            print(f"❌ Resultado inesperado: {result}")
            return render_template('login.html', error="Erro ao fazer login. Verifique suas credenciais.")
        
        print("🚀 Redirecionando para dashboard...")
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
    
    try:
        collector = DataCollector()
        success = await collector.collect_all_data()
        
        if success:
            return redirect(url_for('dashboard'))
        else:
            return "Erro ao sincronizar dados", 500
    except Exception as e:
        print(f"Erro na sincronização: {e}")
        return "Erro interno do servidor", 500

@app.route('/test-collector')
@login_required
@async_route
async def test_collector():
    """Endpoint para testar o coletor de dados."""
    from data_collector import DataCollector
    
    try:
        collector = DataCollector()
        
        # Testa coleta de dados
        sites = await collector.collect_sites()
        devices = await collector.collect_devices()
        alerts = await collector.collect_alerts()
        
        result = {
            'sites_count': len(sites),
            'devices_count': len(devices),
            'alerts_count': len(alerts),
            'sites': sites[:3],  # Primeiros 3 sites
            'devices': devices[:3],  # Primeiros 3 dispositivos
            'alerts': alerts[:3]  # Primeiros 3 alertas
        }
        
        return jsonify(result)
    except Exception as e:
        print(f"Erro no teste do coletor: {e}")
        return jsonify({'error': str(e)}), 500

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
    # Configuração para produção
    if os.getenv("FLASK_ENV") == "production":
        # Usar servidor de produção
        from waitress import serve
        print("🚀 Iniciando servidor de produção...")
        serve(app, host='0.0.0.0', port=5000)
    else:
        # Modo desenvolvimento
        app.run(debug=True, host='0.0.0.0', port=5000)
