import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional, Tuple
import asyncio

load_dotenv()

class SupabaseManager:
    def __init__(self):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()
        
        # Obtém as variáveis de ambiente no formato do EasyPanel
        self.supabase_url: str = os.getenv("SUPABASE_URL")
        self.supabase_key: str = os.getenv("SUPABASE_KEY")
        self.supabase_secret: str = os.getenv("SUPABASE_SECRET")
        
        # Debug apenas em desenvolvimento
        if os.getenv("FLASK_ENV") == "development":
            print("=== DEBUG: Variáveis de Ambiente ===")
            print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
            print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))
            print("SUPABASE_SECRET:", os.getenv("SUPABASE_SECRET"))
            print("===================================")
        
        # Se não estiverem definidas, usa valores padrão para desenvolvimento
        if not self.supabase_url:
            self.supabase_url = "https://pszfqqmmljekibmcgmig.supabase.co"
        if not self.supabase_key:
            self.supabase_key = "sb_publishable_d2NwmSXLau87m9yNp590bA_zOKPvlMX"
        if not self.supabase_secret:
            self.supabase_secret = "sb_secret_9nszt9IAhYd94neHZQHP6w_0viqK_FW"
        
        # Debug apenas em desenvolvimento
        if os.getenv("FLASK_ENV") == "development":
            print(f"SUPABASE_URL: {self.supabase_url[:20] if self.supabase_url else 'None'}...")
            print(f"SUPABASE_KEY: {self.supabase_key[:20] if self.supabase_key else 'None'}...")
            print(f"SUPABASE_SECRET: {self.supabase_secret[:20] if self.supabase_secret else 'None'}...")
            
            # Lista todas as variáveis de ambiente para debug
            print("Variáveis de ambiente disponíveis:")
            for key, value in os.environ.items():
                if 'SUPABASE' in key or 'NEXT_PUBLIC' in key:
                    print(f"  {key}: {value[:20] if value else 'None'}...")
        
        try:
            # Para operações de backend, usa a chave de serviço
            self.client: Client = create_client(self.supabase_url, self.supabase_secret)
            if os.getenv("FLASK_ENV") == "development":
                print("Cliente Supabase criado com sucesso (usando service role key)")
        except Exception as e:
            print(f"Erro ao criar cliente Supabase: {e}")
            if os.getenv("FLASK_ENV") == "development":
                print("URL:", self.supabase_url)
                print("Secret Key:", self.supabase_secret[:20] + "..." if self.supabase_secret else "None")
            # Em caso de erro, cria um cliente mock para desenvolvimento
            if os.getenv("FLASK_ENV") == "development":
                print("Criando cliente mock para desenvolvimento...")
            self.client = None
        
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
            # Se não há cliente, retorna dados mock
            if not self.client:
                mock_devices = [
                    {'uid': '1', 'hostname': 'server-01', 'site_uid': 'site-1', 'status': 'online', 'last_seen': '2024-08-02T10:00:00Z'},
                    {'uid': '2', 'hostname': 'server-02', 'site_uid': 'site-1', 'status': 'offline', 'last_seen': '2024-08-02T09:30:00Z'},
                    {'uid': '3', 'hostname': 'workstation-01', 'site_uid': 'site-2', 'status': 'online', 'last_seen': '2024-08-02T10:15:00Z'},
                ]
                return mock_devices
            
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
            # Se não há cliente, retorna dados mock
            if not self.client:
                return {
                    'total_devices': 25,
                    'online_devices': 18,
                    'offline_devices': 7,
                    'total_alerts': 5,
                    'new_alerts': 2,
                    'total_sites': 3
                }
            
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
                'total_devices': 25,
                'online_devices': 18,
                'offline_devices': 7,
                'total_alerts': 5,
                'new_alerts': 2,
                'total_sites': 3
            }
    
    async def get_recent_devices(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtém dispositivos recentes para o dashboard."""
        try:
            if not self.client:
                return []
            
            response = self.client.table('devices').select('*').order('last_seen', desc=True).limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao obter dispositivos recentes: {e}")
            return []
    
    async def get_recent_alerts(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtém alertas recentes para o dashboard."""
        try:
            if not self.client:
                return []
            
            response = self.client.table('alerts').select('*').order('created_at', desc=True).limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao obter alertas recentes: {e}")
            return []
