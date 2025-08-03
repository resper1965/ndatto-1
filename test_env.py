#!/usr/bin/env python3
"""
Script para testar se as variáveis de ambiente estão sendo carregadas corretamente
"""

import os
from dotenv import load_dotenv

def test_environment_variables():
    """Testa se as variáveis de ambiente estão sendo carregadas"""
    
    print("=== TESTE DE VARIÁVEIS DE AMBIENTE ===")
    
    # Carrega o arquivo .env
    load_dotenv()
    
    # Lista todas as variáveis de ambiente
    print("\nTodas as variáveis de ambiente:")
    for key, value in os.environ.items():
        if 'SUPABASE' in key or 'SECRET' in key or 'FLASK' in key:
            print(f"  {key}: {value[:20] if value else 'None'}...")
    
    # Testa as variáveis específicas
    print("\nVariáveis específicas:")
    variables = {
        'SUPABASE_URL': os.getenv("SUPABASE_URL"),
        'SUPABASE_KEY': os.getenv("SUPABASE_KEY"),
        'SUPABASE_SECRET': os.getenv("SUPABASE_SECRET"),
        'SECRET_KEY': os.getenv("SECRET_KEY"),
        'FLASK_APP': os.getenv("FLASK_APP"),
        'FLASK_ENV': os.getenv("FLASK_ENV")
    }
    
    for key, value in variables.items():
        status = "✅ DEFINIDA" if value else "❌ NÃO DEFINIDA"
        print(f"  {key}: {status}")
        if value:
            print(f"    Valor: {value[:20]}...")
    
    # Testa se as variáveis antigas ainda existem
    print("\nVariáveis antigas (para compatibilidade):")
    old_variables = {
        'NEXT_PUBLIC_SUPABASE_URL': os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
        'NEXT_PUBLIC_SUPABASE_ANON_KEY': os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
        'SUPABASE_SERVICE_ROLE_KEY': os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    }
    
    for key, value in old_variables.items():
        status = "✅ DEFINIDA" if value else "❌ NÃO DEFINIDA"
        print(f"  {key}: {status}")
    
    print("\n=== FIM DO TESTE ===")

if __name__ == "__main__":
    test_environment_variables() 