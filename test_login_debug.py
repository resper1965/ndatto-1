#!/usr/bin/env python3
"""
Script para debugar o processo de login
"""

import os
import asyncio
from dotenv import load_dotenv
from supabase_client import SupabaseManager

load_dotenv()

async def test_login_process():
    """Testa o processo completo de login."""
    print("🧪 Testando processo de login...")
    
    # Inicializa o cliente Supabase
    supabase = SupabaseManager()
    
    # Testa configuração
    print(f"✅ URL: {supabase.supabase_url[:30]}...")
    print(f"✅ Key: {supabase.supabase_key[:20]}...")
    print(f"✅ Secret: {supabase.supabase_secret[:20]}...")
    
    if not supabase.client:
        print("❌ Cliente Supabase não inicializado")
        return False
    
    # Testa login com credenciais de teste
    test_email = "test@ness.com.br"
    test_password = "test_password"
    
    print(f"\n🔍 Testando login com: {test_email}")
    
    try:
        result = await supabase.sign_in(test_email, test_password)
        print(f"📊 Tipo do resultado: {type(result)}")
        
        # Verifica se há erro
        if hasattr(result, 'error') and result.error:
            print(f"❌ Erro no login: {result.error}")
            return False
        
        if isinstance(result, dict) and 'error' in result:
            print(f"❌ Erro no login (dict): {result['error']}")
            return False
        
        # Verifica se tem sessão
        if hasattr(result, 'session') and result.session:
            print("✅ Login bem-sucedido - sessão encontrada")
            print(f"   Access Token: {result.session.access_token[:20]}...")
            print(f"   Refresh Token: {result.session.refresh_token[:20]}...")
            
            if hasattr(result, 'user') and result.user:
                print(f"   Usuário: {result.user.email}")
                print(f"   ID: {result.user.id}")
            else:
                print("⚠️  Usuário não encontrado no resultado")
        else:
            print("❌ Sessão não encontrada no resultado")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

async def test_token_verification():
    """Testa a verificação de token."""
    print("\n🔍 Testando verificação de token...")
    
    supabase = SupabaseManager()
    
    # Testa com token inválido
    try:
        user = await supabase.verify_token("invalid_token")
        if user is None:
            print("✅ Verificação de token inválido retornou None (esperado)")
        else:
            print("⚠️  Verificação de token inválido não retornou None")
    except Exception as e:
        print(f"❌ Erro ao verificar token: {e}")

async def test_supabase_connection():
    """Testa a conexão com o Supabase."""
    print("\n🔍 Testando conexão com Supabase...")
    
    supabase = SupabaseManager()
    
    try:
        # Testa se consegue acessar o cliente
        if supabase.client:
            print("✅ Cliente Supabase criado com sucesso")
            
            # Testa uma operação simples
            try:
                # Tenta obter usuário atual (deve falhar sem autenticação)
                user = await supabase.get_user()
                if user is None:
                    print("✅ get_user retornou None (esperado sem autenticação)")
                else:
                    print(f"⚠️  get_user retornou: {user}")
            except Exception as e:
                print(f"⚠️  get_user falhou (esperado): {e}")
        else:
            print("❌ Cliente Supabase não foi criado")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False
    
    return True

async def main():
    """Função principal."""
    print("🚀 Iniciando debug do processo de login...")
    print("=" * 50)
    
    # Testa conexão
    connection_ok = await test_supabase_connection()
    
    if connection_ok:
        # Testa processo de login
        login_ok = await test_login_process()
        
        # Testa verificação de token
        await test_token_verification()
        
        print("\n" + "=" * 50)
        print("📊 Resumo dos testes:")
        print(f"   Conexão: {'✅ OK' if connection_ok else '❌ FALHOU'}")
        print(f"   Login: {'✅ OK' if login_ok else '❌ FALHOU'}")
        
        if connection_ok and login_ok:
            print("\n🎉 Todos os testes passaram!")
            print("💡 Se o login não está funcionando na web, verifique:")
            print("   1. Se as credenciais estão corretas")
            print("   2. Se o domínio @ness.com.br está sendo aceito")
            print("   3. Se há erros no console do navegador")
            print("   4. Se há erros nos logs da aplicação")
        else:
            print("\n⚠️  Alguns testes falharam. Verifique a configuração.")
    else:
        print("\n❌ Problema na conexão com Supabase")

if __name__ == "__main__":
    asyncio.run(main()) 