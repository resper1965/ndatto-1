#!/usr/bin/env python3
"""
Script para testar a integração com a API do Datto RMM
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()

class DattoAPITester:
    def __init__(self):
        self.api_key = os.getenv("DATTO_API_KEY")
        self.api_secret = os.getenv("DATTO_API_SECRET")
        self.base_url = "https://centraapi.centrastage.net/api/v2"
        
        print("🔧 Configuração da API Datto:")
        print(f"   API Key: {self.api_key[:10]}..." if self.api_key else "❌ Não configurada")
        print(f"   API Secret: {self.api_secret[:10]}..." if self.api_secret else "❌ Não configurada")
        print(f"   Base URL: {self.base_url}")
        print()
    
    async def test_connection(self):
        """Testa a conexão com a API do Datto."""
        print("🔍 Testando conexão com a API Datto...")
        
        if not self.api_key or not self.api_secret:
            print("❌ Chaves da API não configuradas!")
            print("Configure DATTO_API_KEY e DATTO_API_SECRET no arquivo .env")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Testa endpoint básico
                async with session.get(f"{self.base_url}/account", headers=headers) as response:
                    print(f"📡 Status da resposta: {response.status}")
                    
                    if response.status == 200:
                        data = await response.json()
                        print("✅ Conexão com a API estabelecida!")
                        print(f"   Resposta: {data}")
                        return True
                    elif response.status == 401:
                        print("❌ Erro de autenticação - verifique as chaves da API")
                        return False
                    elif response.status == 403:
                        print("❌ Acesso negado - verifique as permissões da API")
                        return False
                    else:
                        print(f"❌ Erro inesperado: {response.status}")
                        print(f"   Resposta: {await response.text()}")
                        return False
                        
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False
    
    async def test_endpoints(self):
        """Testa os principais endpoints da API."""
        print("\n🔍 Testando endpoints da API...")
        
        if not self.api_key or not self.api_secret:
            print("❌ Chaves da API não configuradas!")
            return
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        endpoints = [
            "account",
            "sites", 
            "devices",
            "alerts"
        ]
        
        async with aiohttp.ClientSession() as session:
            for endpoint in endpoints:
                try:
                    print(f"\n📡 Testando endpoint: /{endpoint}")
                    async with session.get(f"{self.base_url}/{endpoint}", headers=headers) as response:
                        print(f"   Status: {response.status}")
                        
                        if response.status == 200:
                            data = await response.json()
                            if isinstance(data, dict) and 'data' in data:
                                print(f"   ✅ Sucesso! {len(data['data'])} registros encontrados")
                            else:
                                print(f"   ✅ Sucesso! Resposta: {data}")
                        else:
                            print(f"   ❌ Erro: {response.status}")
                            print(f"   Resposta: {await response.text()}")
                            
                except Exception as e:
                    print(f"   ❌ Erro ao testar {endpoint}: {e}")
    
    async def test_data_collector(self):
        """Testa o coletor de dados."""
        print("\n🧪 Testando o coletor de dados...")
        
        try:
            from data_collector import DataCollector
            
            collector = DataCollector()
            
            # Testa coleta de sites
            print("📊 Coletando sites...")
            sites = await collector.collect_sites()
            print(f"   Sites encontrados: {len(sites)}")
            
            # Testa coleta de dispositivos
            print("💻 Coletando dispositivos...")
            devices = await collector.collect_devices()
            print(f"   Dispositivos encontrados: {len(devices)}")
            
            # Testa coleta de alertas
            print("🚨 Coletando alertas...")
            alerts = await collector.collect_alerts()
            print(f"   Alertas encontrados: {len(alerts)}")
            
            # Testa estatísticas
            print("📈 Calculando estatísticas...")
            stats = await collector.collect_realtime_data()
            print(f"   Estatísticas: {stats}")
            
            print("✅ Teste do coletor concluído!")
            
        except Exception as e:
            print(f"❌ Erro no teste do coletor: {e}")
    
    async def run_all_tests(self):
        """Executa todos os testes."""
        print("🚀 Iniciando testes da API Datto...")
        print("=" * 50)
        
        # Testa conexão
        connection_ok = await self.test_connection()
        
        if connection_ok:
            # Testa endpoints
            await self.test_endpoints()
            
            # Testa coletor de dados
            await self.test_data_collector()
        else:
            print("\n⚠️  Pulando testes de endpoints devido a erro de conexão")
        
        print("\n" + "=" * 50)
        print("🏁 Testes concluídos!")

async def main():
    """Função principal."""
    tester = DattoAPITester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 