#!/usr/bin/env python3
"""
Script para testar a autenticação do Supabase
"""

import os
import asyncio
from dotenv import load_dotenv
from supabase_client import SupabaseManager

load_dotenv()

async def test_supabase_auth():
    """Testa a autenticação do Supabase."""
    print("🧪 Testando autenticação do Supabase...")
    
    # Inicializa o cliente Supabase
    supabase = SupabaseManager()
    
    # Testa configuração
    print(f"✅ URL: {supabase.supabase_url[:30]}...")
    print(f"✅ Key: {supabase.supabase_key[:20]}...")
    print(f"✅ Secret: {supabase.supabase_secret[:20]}...")
    
    # Testa se o cliente foi criado
    if supabase.client:
        print("✅ Cliente Supabase criado com sucesso")
    else:
        print("❌ Erro ao criar cliente Supabase")
        return False
    
    # Testa sign_in com credenciais inválidas (deve retornar erro)
    print("\n🔍 Testando login com credenciais inválidas...")
    try:
        result = await supabase.sign_in("test@ness.com.br", "wrong_password")
        if hasattr(result, 'error') or (isinstance(result, dict) and 'error' in result):
            print("✅ Login com credenciais inválidas retornou erro (esperado)")
        else:
            print("⚠️  Login com credenciais inválidas não retornou erro")
    except Exception as e:
        print(f"❌ Erro ao testar login: {e}")
    
    # Testa verify_token com token inválido
    print("\n🔍 Testando verificação de token inválido...")
    try:
        user = await supabase.verify_token("invalid_token")
        if user is None:
            print("✅ Verificação de token inválido retornou None (esperado)")
        else:
            print("⚠️  Verificação de token inválido não retornou None")
    except Exception as e:
        print(f"❌ Erro ao verificar token: {e}")
    
    # Testa get_user
    print("\n🔍 Testando get_user...")
    try:
        user = await supabase.get_user()
        if user is None:
            print("✅ get_user retornou None (esperado sem autenticação)")
        else:
            print(f"⚠️  get_user retornou: {user}")
    except Exception as e:
        print(f"❌ Erro ao obter usuário: {e}")
    
    print("\n✅ Teste de autenticação concluído!")
    return True

async def test_data_collector():
    """Testa o coletor de dados."""
    print("\n🧪 Testando coletor de dados...")
    
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
        
        print("✅ Teste do coletor concluído!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do coletor: {e}")
        return False

async def main():
    """Função principal."""
    print("🚀 Iniciando testes do sistema NCISO...")
    print("=" * 50)
    
    # Testa autenticação
    auth_ok = await test_supabase_auth()
    
    # Testa coletor de dados
    collector_ok = await test_data_collector()
    
    print("\n" + "=" * 50)
    print("📊 Resumo dos testes:")
    print(f"   Autenticação: {'✅ OK' if auth_ok else '❌ FALHOU'}")
    print(f"   Coletor: {'✅ OK' if collector_ok else '❌ FALHOU'}")
    
    if auth_ok and collector_ok:
        print("\n🎉 Todos os testes passaram!")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique a configuração.")

if __name__ == "__main__":
    asyncio.run(main()) 