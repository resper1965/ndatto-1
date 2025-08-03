#!/bin/bash

echo "🔍 TESTANDO TODAS AS PORTAS POSSÍVEIS"
echo "======================================"
echo ""

# Array de portas para testar
portas=(3000 5000 8080 8000 80 443)

for porta in "${portas[@]}"; do
    echo "🧪 Testando porta $porta..."
    
    # Teste básico de conectividade
    status=$(curl -s -o /dev/null -w "%{http_code}" http://62.72.8.164:$porta/ 2>/dev/null)
    
    if [ "$status" = "000" ]; then
        echo "   ❌ Porta $porta: Não responde"
    else
        echo "   ✅ Porta $porta: Status $status"
        
        # Se responde, testar endpoints específicos
        if [ "$status" != "000" ]; then
            echo "   🔍 Testando endpoints na porta $porta..."
            
            # Teste /api/health
            health_status=$(curl -s -o /dev/null -w "%{http_code}" http://62.72.8.164:$porta/api/health 2>/dev/null)
            echo "      /api/health: $health_status"
            
            # Teste /api/devices
            devices_status=$(curl -s -o /dev/null -w "%{http_code}" http://62.72.8.164:$porta/api/devices 2>/dev/null)
            echo "      /api/devices: $devices_status"
            
            # Teste resposta completa
            echo "      📄 Resposta completa:"
            curl -s http://62.72.8.164:$porta/ | head -3
        fi
    fi
    
    echo ""
done

echo "✅ Teste de portas concluído!" 