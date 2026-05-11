#!/home/volbiobio/virtualenv/api/3.12/bin/python3.12_bin
# -*- coding: utf-8 -*-

import sys
import os

def run_migrations():
    # Configurar paths
    BASE_DIR = '/home/volbiobio/services'
    VENV_SITE = '/home/volbiobio/virtualenv/services/3.12/lib/python3.12/site-packages'

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