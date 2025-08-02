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
        
        # Debug: imprime as variáveis (sem mostrar valores completos)
        print(f"SUPABASE_URL: {self.supabase_url[:20] if self.supabase_url else 'None'}...")
        print(f"SUPABASE_KEY: {self.supabase_key[:20] if self.supabase_key else 'None'}...")
        
        # Verifica se as variáveis de ambiente estão definidas
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidos nas variáveis de ambiente")
        
        try:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
            print("Cliente Supabase criado com sucesso")
        except Exception as e:
            print(f"Erro ao criar cliente Supabase: {e}")
            raise
        
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
