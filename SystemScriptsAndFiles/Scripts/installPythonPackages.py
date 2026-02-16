#!/home/volbiobio/virtualenv/api/3.13/bin/python3.13_bin
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import glob

def install_packages():
    os.chdir('/home/volbiobio/api')

    python_path = '/home/volbiobio/virtualenv/api/3.13/bin/python3.13_bin'
    pip_path = '/home/volbiobio/virtualenv/api/3.13/bin/pip'

    print("=" * 60)
    print("REINSTALACIÓN FORZADA DE PAQUETES")
    print("=" * 60)

    # Verificar que pip existe
    if not os.path.exists(pip_path):
        print(f"⚠️  pip no encontrado en {pip_path}")
        print("   Usando: python -m pip")
        pip_cmd = [python_path, '-m', 'pip']
    else:
        pip_cmd = [pip_path]

    # Actualizar pip
    print("\n1. Actualizando pip...")
    result = subprocess.run(
        pip_cmd + ['install', '--upgrade', 'pip'],
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Obtener archivos .whl
    whl_files = sorted(glob.glob('packages/*.whl'))

    if not whl_files:
        print("\n❌ NO se encontraron archivos .whl en packages/")
        sys.exit(1)

    print(f"\n2. Instalando {len(whl_files)} paquetes desde archivos locales...")
    print("=" * 60)

    # Instalar todos los .whl
    for whl in whl_files:
        pkg_name = os.path.basename(whl)
        print(f"\n📦 {pkg_name}")
        
        result = subprocess.run(
            pip_cmd + ['install', '--force-reinstall', '--no-deps', whl],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("   ✅ Instalado")
        else:
            print(f"   ❌ Error: {result.stderr[:200]}")

    # Verificar instalación
    print("\n" + "=" * 60)
    print("3. Verificando instalación...")
    print("=" * 60)

    result = subprocess.run(
        pip_cmd + ['list'],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    # Verificar Django específicamente
    print("\n" + "=" * 60)
    print("4. Verificando Django...")
    print("=" * 60)

    result = subprocess.run(
        [python_path, '-c', 'import django; print(f"Django {django.__version__} instalado correctamente")'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"✅ {result.stdout.strip()}")
    else:
        print(f"❌ Error: {result.stderr}")

    print("\n" + "=" * 60)
    print("✅ REINSTALACIÓN COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    install_packages()
