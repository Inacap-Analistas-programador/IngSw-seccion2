#!/home/volbiobio/virtualenv/api/3.13/bin/python3.13_bin
# -*- coding: utf-8 -*-

import sys
import os

def run_migrations():
    # Configurar paths
    BASE_DIR = '/home/volbiobio/api'
    VENV_SITE = '/home/volbiobio/virtualenv/api/3.13/lib/python3.13/site-packages'

    sys.path.insert(0, BASE_DIR)
    sys.path.insert(0, VENV_SITE)

    os.chdir(BASE_DIR)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')

    print("=" * 60)
    print("EJECUTANDO MIGRACIONES")
    print("=" * 60)

    try:
        import django
        django.setup()
        
        from django.core.management import call_command
        
        # Ejecutar migraciones
        print("\n📊 Ejecutando migrate...")
        call_command('migrate', '--noinput', verbosity=2)
        
        print("\n✅ MIGRACIONES COMPLETADAS")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_migrations()