from flask import Flask, render_template, request, jsonify, redirect, url_for
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

# Configurações de produção
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Configuração CORS - permite todos os domínios
CORS(app)



# Inicializa o gerenciador do Supabase
supabase = SupabaseManager()

def async_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@app.route('/')
@async_route
async def dashboard():
    try:
        # Obtém estatísticas do dashboard
        stats = await supabase.get_dashboard_stats()
        
        # Obtém dados recentes
        recent_devices = await supabase.get_recent_devices(5)
        recent_alerts = await supabase.get_recent_alerts(5)
        
        return render_template(
            'dashboard.html',
            stats=stats,
            recent_devices=recent_devices,
            recent_alerts=recent_alerts,
            user={'email': 'admin@ness.com.br'}  # Usuário mock para compatibilidade
        )
    except Exception as e:
        print(f"❌ Erro no dashboard: {e}")
        return render_template('dashboard.html', error=str(e))

@app.route('/login')
def login_404():
    """Retorna 404 para /login - sistema sem autenticação"""
    return "Página não encontrada - Sistema sem autenticação", 404



@app.route('/devices')
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
@async_route
async def alerts():
    page = request.args.get('page', 1, type=int)
    severity = request.args.get('severity', '')
    status = request.args.get('status', '')
    
    filters = {}
    if severity:
        filters['severity'] = severity
    if status:
        filters['status'] = status
    
    alerts = await supabase.get_alerts(filters)
    
    return render_template(
        'alerts.html',
        alerts=alerts,
        current_page=page,
        severity=severity,
        status=status
    )

@app.route('/resolve_alert/<alert_uid>')
@async_route
async def resolve_alert_route(alert_uid):
    success = await supabase.resolve_alert(alert_uid)
    if success:
        return redirect(url_for('alerts'))
    else:
        return "Erro ao resolver alerta", 400

@app.route('/sites')
@async_route
async def sites():
    sites = await supabase.get_sites()
    return render_template('sites.html', sites=sites)

@app.route('/sync')
@async_route
async def sync_data():
    try:
        from data_collector import DataCollector
        collector = DataCollector()
        success = await collector.collect_all_data()
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Dados sincronizados com sucesso!',
                'timestamp': '2025-01-27T10:00:00Z'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erro ao sincronizar dados',
                'timestamp': '2025-01-27T10:00:00Z'
            }), 500
    except Exception as e:
        print(f"❌ Erro na sincronização: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro interno: {str(e)}',
            'timestamp': '2025-01-27T10:00:00Z'
        }), 500

@app.route('/test-collector')
@async_route
async def test_collector():
    try:
        from data_collector import DataCollector
        collector = DataCollector()
        
        # Testa coleta de dados
        sites = await collector.collect_sites()
        devices = await collector.collect_devices()
        alerts = await collector.collect_alerts()
        
        return jsonify({
            'status': 'success',
            'data': {
                'sites_count': len(sites),
                'devices_count': len(devices),
                'alerts_count': len(alerts),
                'sites': sites[:3],  # Primeiros 3 sites
                'devices': devices[:3],  # Primeiros 3 devices
                'alerts': alerts[:3]  # Primeiros 3 alerts
            },
            'message': 'Teste do coletor de dados realizado com sucesso!',
            'timestamp': '2025-01-27T10:00:00Z'
        })
    except Exception as e:
        print(f"❌ Erro no teste do coletor: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro no teste: {str(e)}',
            'timestamp': '2025-01-27T10:00:00Z'
        }), 500

@app.route('/api/user')
@async_route
async def get_user():
    return jsonify({
        'id': 'admin-user',
        'email': 'admin@ness.com.br',
        'role': 'admin',
        'authenticated': True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
