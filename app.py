from flask import Flask, render_template, request, jsonify, redirect, url_for, session
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
