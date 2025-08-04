import os
import asyncio
import aiohttp
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from supabase_client import SupabaseManager

load_dotenv()

class DataCollector:
    def __init__(self):
        self.api_key = os.getenv("DATTO_API_KEY")
        self.api_secret = os.getenv("DATTO_API_SECRET")
        self.base_url = "https://centraapi.centrastage.net/api/v2"
        self.supabase = SupabaseManager()
        
        if not self.api_key or not self.api_secret:
            print("⚠️  AVISO: Chaves da API Datto não configuradas")
            print("Configure DATTO_API_KEY e DATTO_API_SECRET no arquivo .env")
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Faz uma requisição para a API do Datto."""
        if not self.api_key or not self.api_secret:
            print(f"❌ Erro: Chaves da API Datto não configuradas")
            return None
        
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"❌ Erro na API Datto: {response.status} - {await response.text()}")
                        return None
        except Exception as e:
            print(f"❌ Erro ao fazer requisição para {endpoint}: {e}")
            return None
    
    async def collect_sites(self) -> List[Dict[str, Any]]:
        """Coleta dados dos sites do Datto."""
        print("🔍 Coletando sites...")
        
        try:
            # Simula dados de sites (substitua pela API real do Datto)
            sites_data = await self._make_request("sites")
            
            if not sites_data:
                # Dados mock para desenvolvimento
                sites_data = {
                    "data": [
                        {
                            "uid": "site-001",
                            "name": "Matriz - São Paulo",
                            "address": "Rua das Flores, 123 - São Paulo/SP",
                            "status": "active",
                            "device_count": 15
                        },
                        {
                            "uid": "site-002", 
                            "name": "Filial - Rio de Janeiro",
                            "address": "Av. Copacabana, 456 - Rio de Janeiro/RJ",
                            "status": "active",
                            "device_count": 8
                        },
                        {
                            "uid": "site-003",
                            "name": "Filial - Belo Horizonte", 
                            "address": "Rua da Liberdade, 789 - Belo Horizonte/MG",
                            "status": "active",
                            "device_count": 12
                        }
                    ]
                }
            
            sites = []
            for site in sites_data.get("data", []):
                site_data = {
                    "uid": site.get("uid"),
                    "name": site.get("name"),
                    "address": site.get("address"),
                    "status": site.get("status", "active"),
                    "device_count": site.get("device_count", 0),
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                sites.append(site_data)
            
            print(f"✅ {len(sites)} sites coletados")
            return sites
            
        except Exception as e:
            print(f"❌ Erro ao coletar sites: {e}")
            return []
    
    async def collect_devices(self) -> List[Dict[str, Any]]:
        """Coleta dados dos dispositivos do Datto."""
        print("🔍 Coletando dispositivos...")
        
        try:
            # Simula dados de dispositivos (substitua pela API real do Datto)
            devices_data = await self._make_request("devices")
            
            if not devices_data:
                # Dados mock para desenvolvimento
                devices_data = {
                    "data": [
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
                        },
                        {
                            "uid": "dev-002",
                            "hostname": "workstation-rj-01", 
                            "site_uid": "site-002",
                            "status": "online",
                            "ip_address": "192.168.2.50",
                            "last_seen": "2024-01-15T10:25:00Z",
                            "os": "Windows 11",
                            "memory": "8GB",
                            "cpu": "Intel i5"
                        },
                        {
                            "uid": "dev-003",
                            "hostname": "server-bh-01",
                            "site_uid": "site-003", 
                            "status": "offline",
                            "ip_address": "192.168.3.75",
                            "last_seen": "2024-01-15T09:45:00Z",
                            "os": "Ubuntu 20.04",
                            "memory": "32GB",
                            "cpu": "AMD EPYC"
                        },
                        {
                            "uid": "dev-004",
                            "hostname": "workstation-sp-02",
                            "site_uid": "site-001",
                            "status": "online", 
                            "ip_address": "192.168.1.101",
                            "last_seen": "2024-01-15T10:28:00Z",
                            "os": "Windows 10",
                            "memory": "16GB",
                            "cpu": "Intel i7"
                        },
                        {
                            "uid": "dev-005",
                            "hostname": "server-rj-01",
                            "site_uid": "site-002",
                            "status": "online",
                            "ip_address": "192.168.2.100", 
                            "last_seen": "2024-01-15T10:32:00Z",
                            "os": "Windows Server 2022",
                            "memory": "64GB",
                            "cpu": "Intel Xeon"
                        }
                    ]
                }
            
            devices = []
            for device in devices_data.get("data", []):
                device_data = {
                    "uid": device.get("uid"),
                    "hostname": device.get("hostname"),
                    "site_uid": device.get("site_uid"),
                    "status": device.get("status", "unknown"),
                    "ip_address": device.get("ip_address"),
                    "last_seen": device.get("last_seen"),
                    "os": device.get("os"),
                    "memory": device.get("memory"),
                    "cpu": device.get("cpu"),
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                devices.append(device_data)
            
            print(f"✅ {len(devices)} dispositivos coletados")
            return devices
            
        except Exception as e:
            print(f"❌ Erro ao coletar dispositivos: {e}")
            return []
    
    async def collect_alerts(self) -> List[Dict[str, Any]]:
        """Coleta alertas do Datto."""
        print("🔍 Coletando alertas...")
        
        try:
            # Simula dados de alertas (substitua pela API real do Datto)
            alerts_data = await self._make_request("alerts")
            
            if not alerts_data:
                # Dados mock para desenvolvimento
                alerts_data = {
                    "data": [
                        {
                            "uid": "alert-001",
                            "device_uid": "dev-003",
                            "alert_type": "device_offline",
                            "severity": "high",
                            "status": "new",
                            "message": "Dispositivo server-bh-01 está offline há mais de 30 minutos",
                            "created_at": "2024-01-15T09:45:00Z"
                        },
                        {
                            "uid": "alert-002",
                            "device_uid": "dev-001", 
                            "alert_type": "high_cpu_usage",
                            "severity": "medium",
                            "status": "new",
                            "message": "CPU usage acima de 90% no servidor server-sp-01",
                            "created_at": "2024-01-15T10:15:00Z"
                        },
                        {
                            "uid": "alert-003",
                            "device_uid": "dev-004",
                            "alert_type": "low_disk_space",
                            "severity": "low", 
                            "status": "resolved",
                            "message": "Espaço em disco baixo no workstation-sp-02",
                            "created_at": "2024-01-15T09:30:00Z"
                        },
                        {
                            "uid": "alert-004",
                            "device_uid": "dev-002",
                            "alert_type": "security_update",
                            "severity": "medium",
                            "status": "new",
                            "message": "Atualizações de segurança pendentes no workstation-rj-01",
                            "created_at": "2024-01-15T10:00:00Z"
                        }
                    ]
                }
            
            alerts = []
            for alert in alerts_data.get("data", []):
                alert_data = {
                    "uid": alert.get("uid"),
                    "device_uid": alert.get("device_uid"),
                    "alert_type": alert.get("alert_type"),
                    "severity": alert.get("severity", "low"),
                    "status": alert.get("status", "new"),
                    "message": alert.get("message"),
                    "created_at": alert.get("created_at")
                }
                alerts.append(alert_data)
            
            print(f"✅ {len(alerts)} alertas coletados")
            return alerts
            
        except Exception as e:
            print(f"❌ Erro ao coletar alertas: {e}")
            return []
    
    async def collect_device_components(self, device_uid: str) -> List[Dict[str, Any]]:
        """Coleta componentes de um dispositivo específico."""
        print(f"🔍 Coletando componentes do dispositivo {device_uid}...")
        
        try:
            # Simula dados de componentes (substitua pela API real do Datto)
            components_data = await self._make_request(f"devices/{device_uid}/components")
            
            if not components_data:
                # Dados mock para desenvolvimento
                components_data = {
                    "data": [
                        {
                            "uid": "comp-001",
                            "name": "CPU",
                            "type": "processor",
                            "status": "healthy",
                            "details": "Intel Xeon E5-2680 v4 @ 2.40GHz"
                        },
                        {
                            "uid": "comp-002",
                            "name": "Memory",
                            "type": "memory", 
                            "status": "healthy",
                            "details": "16GB DDR4"
                        },
                        {
                            "uid": "comp-003",
                            "name": "Disk C:",
                            "type": "storage",
                            "status": "warning",
                            "details": "500GB SSD - 85% used"
                        },
                        {
                            "uid": "comp-004",
                            "name": "Network Interface",
                            "type": "network",
                            "status": "healthy", 
                            "details": "Gigabit Ethernet"
                        }
                    ]
                }
            
            components = []
            for component in components_data.get("data", []):
                component_data = {
                    "uid": component.get("uid"),
                    "device_uid": device_uid,
                    "name": component.get("name"),
                    "type": component.get("type"),
                    "status": component.get("status", "unknown"),
                    "details": component.get("details"),
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                components.append(component_data)
            
            print(f"✅ {len(components)} componentes coletados")
            return components
            
        except Exception as e:
            print(f"❌ Erro ao coletar componentes: {e}")
            return []
    
    async def save_to_supabase(self, data: List[Dict], table_name: str) -> bool:
        """Salva dados no Supabase."""
        try:
            if not data:
                print(f"⚠️  Nenhum dado para salvar na tabela {table_name}")
                return True
            
            # Limpa dados existentes (para sincronização completa)
            if table_name in ['devices', 'alerts', 'sites']:
                await self.supabase.client.table(table_name).delete().neq('uid', '').execute()
                print(f"🗑️  Dados antigos removidos da tabela {table_name}")
            
            # Insere novos dados
            response = await self.supabase.client.table(table_name).insert(data).execute()
            
            if response.data:
                print(f"✅ {len(response.data)} registros salvos na tabela {table_name}")
                return True
            else:
                print(f"❌ Erro ao salvar dados na tabela {table_name}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao salvar dados na tabela {table_name}: {e}")
            return False
    
    async def collect_all_data(self) -> bool:
        """Coleta todos os dados do Datto e salva no Supabase."""
        print("🚀 Iniciando coleta completa de dados do Datto...")
        
        try:
            # Coleta sites
            sites = await self.collect_sites()
            if sites:
                await self.save_to_supabase(sites, 'sites')
            
            # Coleta dispositivos
            devices = await self.collect_devices()
            if devices:
                await self.save_to_supabase(devices, 'devices')
            
            # Coleta alertas
            alerts = await self.collect_alerts()
            if alerts:
                await self.save_to_supabase(alerts, 'alerts')
            
            # Coleta componentes para cada dispositivo
            for device in devices:
                components = await self.collect_device_components(device['uid'])
                if components:
                    await self.save_to_supabase(components, 'device_components')
            
            print("✅ Coleta de dados concluída com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro durante a coleta de dados: {e}")
            return False
    
    async def collect_realtime_data(self) -> Dict[str, Any]:
        """Coleta dados em tempo real para o dashboard."""
        print("🔄 Coletando dados em tempo real...")
        
        try:
            # Coleta estatísticas básicas
            devices = await self.collect_devices()
            alerts = await self.collect_alerts()
            
            stats = {
                'total_devices': len(devices),
                'online_devices': len([d for d in devices if d.get('status') == 'online']),
                'offline_devices': len([d for d in devices if d.get('status') == 'offline']),
                'total_alerts': len(alerts),
                'new_alerts': len([a for a in alerts if a.get('status') == 'new']),
                'total_sites': len(await self.collect_sites())
            }
            
            print(f"✅ Estatísticas atualizadas: {stats}")
            return stats
            
        except Exception as e:
            print(f"❌ Erro ao coletar dados em tempo real: {e}")
            return {
                'total_devices': 0,
                'online_devices': 0,
                'offline_devices': 0,
                'total_alerts': 0,
                'new_alerts': 0,
                'total_sites': 0
            }

# Função para teste local
async def test_collector():
    """Função para testar o coletor localmente."""
    collector = DataCollector()
    
    print("🧪 Testando coletor de dados...")
    
    # Testa coleta de sites
    sites = await collector.collect_sites()
    print(f"Sites coletados: {len(sites)}")
    
    # Testa coleta de dispositivos
    devices = await collector.collect_devices()
    print(f"Dispositivos coletados: {len(devices)}")
    
    # Testa coleta de alertas
    alerts = await collector.collect_alerts()
    print(f"Alertas coletados: {len(alerts)}")
    
    # Testa dados em tempo real
    stats = await collector.collect_realtime_data()
    print(f"Estatísticas: {stats}")

if __name__ == "__main__":
    asyncio.run(test_collector()) 