#!/usr/bin/env python3
"""
Script para instalar todas las dependencias del archivo requirements.txt

Este script lee el archivo requirements.txt y instala todas las librerías
usando pip. Incluye manejo de errores y progreso visual.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """
    Instala todas las dependencias del archivo requirements.txt
    """
    print("🚀 Iniciando instalación de dependencias...")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ Error: No se encontró el archivo requirements.txt")
        print("   Asegúrate d2e ejecutar este script1 desde el directorio del backend")
        return False
    
    # Leer el archivo requirements.txt
    try:
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"📦 Encontradas {len(requirements)} dependencias para instalar")
        print()
    
    except Exception as e:
        print(f"❌ Error al leer requirements.txt: {e}")
        return False
    
    # Instalar cada dependencia
    successful_installations = 0
    failed_installations = 0
    
    for i, requirement in enumerate(requirements, 1):
        print(f"📥 Instalando ({i}/{len(requirements)}): {requirement}")
        
        try:
            # Ejecutar pip install
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", requirement],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ {requirement} instalado correctamente")
            successful_installations += 1
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al instalar {requirement}:")
            print(f"   {e.stderr}")
            failed_installations += 1
            
        except Exception as e:
            print(f"❌ Error inesperado al instalar {requirement}: {e}")
            failed_installations += 1
        
        print("-" * 40)
    
    # Resumen final
    print("=" * 50)
    print("📊 RESUMEN DE INSTALACIÓN")
    print("=" * 50)
    print(f"✅ Instalaciones exitosas: {successful_installations}")
    print(f"❌ Instalaciones fallidas: {failed_installations}")
    print(f"📦 Total de dependencias: {len(requirements)}")
    
    if failed_installations == 0:
        print("\n🎉 ¡Todas las dependencias se instalaron correctamente!")
        print("   Puedes ejecutar tu aplicación FastAPI ahora.")
        return True
    else:
        print(f"\n⚠️  {failed_installations} dependencias fallaron al instalarse.")
        print("   Revisa los errores arriba y intenta instalar manualmente las que fallaron.")
        return False

def install_all_at_once():
    """
    Instala todas las dependencias de una vez usando pip install -r
    """
    print("🚀 Instalando todas las dependencias de una vez...")
    print("=" * 50)
    
    try:
        # Ejecutar pip install -r requirements.txt
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ Todas las dependencias se instalaron correctamente!")
        print("\n📋 Salida de pip:")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Error al instalar las dependencias:")
        print(e.stderr)
        return False
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """
    Función principal que ejecuta la instalación
    """
    print("🐍 Instalador de Dependencias para FastAPI Backend")
    print("=" * 50)
    
    # Verificar que pip está disponible
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ Error: pip no está disponible")
        print("   Asegúrate de tener Python y pip instalados correctamente")
        return
    
    # Opción 1: Instalar todo de una vez (más rápido)
    print("¿Cómo quieres instalar las dependencias?")
    print("1. Instalar todo de una vez (recomendado)")
    print("2. Instalar una por una (más detallado)")
    
    try:
        choice = input("\nElige una opción (1 o 2): ").strip()
        
        if choice == "1":
            success = install_all_at_once()
        elif choice == "2":
            success = install_requirements()
        else:
            print("❌ Opción inválida. Usando instalación de una vez...")
            success = install_all_at_once()
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Instalación cancelada por el usuario")
        return
    
    if success:
        print("\n🎯 Próximos pasos:")
        print("1. Configura tu archivo .env con las variables de entorno")
        print("2. Ejecuta las migraciones: alembic upgrade head")
        print("3. Inicia el servidor: uvicorn main:app --reload")
    else:
        print("\n💡 Consejos para resolver problemas:")
        print("1. Actualiza pip: python -m pip install --upgrade pip")
        print("2. Instala las dependencias manualmente: pip install -r requirements.txt")
        print("3. Verifica que tienes Python 3.8+ instalado")

if __name__ == "__main__":
    main() 