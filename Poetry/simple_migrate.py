#!/usr/bin/env python3
"""
Script simple para migrar requirements.txt a Poetry
Busca requirements.txt en la misma carpeta donde está este script y ejecuta los comandos de Poetry automáticamente.
"""

import os
import re
import sys
from pathlib import Path
import subprocess

def check_and_migrate():
    """
    Verifica si existe requirements.txt en la carpeta del script, genera y ejecuta comandos de Poetry
    """
    # Obtener la ruta absoluta de la carpeta donde está este script
    script_dir = Path(__file__).parent.resolve()
    req_path = script_dir / 'requirements.txt'

    # Verificar si existe requirements.txt en la carpeta del script
    if not req_path.exists():
        print(f"❌ No se encontró requirements.txt en: {req_path}")
        return

    print(f"✅ Encontrado requirements.txt en: {req_path}")

    # Leer y parsear requirements.txt
    requirements = []
    dev_libs = {'pytest', 'black', 'flake8', 'mypy', 'pytest-cov'}

    with open(req_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Extraer nombre y versión
                if '==' in line:
                    name, version = line.split('==', 1)
                    requirements.append((name, version))
                else:
                    name = line.split('==')[0]
                    requirements.append((name, None))

    if not requirements:
        print("❌ No se encontraron librerías válidas")
        return

    print(f"📦 Encontradas {len(requirements)} librerías")

    # Generar comandos de Poetry
    print("\n🎯 Ejecutando comandos Poetry:")
    print("="*40)

    # Librerías de producción
    prod_libs = [req for req in requirements if req[0].lower() not in dev_libs]
    if prod_libs:
        print("\n📦 Librerías de producción:")
        for name, version in prod_libs:
            if version:
                cmd = ["poetry", "add", f"{name}=={version}"]
            else:
                cmd = ["poetry", "add", name]
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, cwd=script_dir)

    # Librerías de desarrollo
    dev_libs_found = [req for req in requirements if req[0].lower() in dev_libs]
    if dev_libs_found:
        print("\n🛠️ Librerías de desarrollo:")
        for name, version in dev_libs_found:
            if version:
                cmd = ["poetry", "add", "--group", "dev", f"{name}=={version}"]
            else:
                cmd = ["poetry", "add", "--group", "dev", name]
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, cwd=script_dir)

    print("\n🚀 Pasos para completar:")
    print("1. poetry install")
    print("2. poetry shell")

if __name__ == "__main__":
    check_and_migrate() 