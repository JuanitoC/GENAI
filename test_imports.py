#!/usr/bin/env python3
"""
Script de prueba para verificar que las importaciones de CrewAI funcionan correctamente
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("🔍 Probando importaciones de CrewAI...")

try:
    print("1. Importando crewai.flow.flow...")
    from crewai.flow.flow import Flow, listen, start
    print("✅ crewai.flow.flow importado correctamente")
except Exception as e:
    print(f"❌ Error importando crewai.flow.flow: {e}")

try:
    print("2. Importando litellm...")
    from litellm import completion
    print("✅ litellm importado correctamente")
except Exception as e:
    print(f"❌ Error importando litellm: {e}")

try:
    print("3. Importando crewai.agent...")
    from crewai.agent import Agent
    print("✅ crewai.agent importado correctamente")
except Exception as e:
    print(f"❌ Error importando crewai.agent: {e}")

try:
    print("4. Verificando OPENAI_API_KEY...")
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OPENAI_API_KEY encontrada")
    else:
        print("⚠️  OPENAI_API_KEY no encontrada")
except Exception as e:
    print(f"❌ Error verificando OPENAI_API_KEY: {e}")

print("\n🎉 Prueba de importaciones completada!") 