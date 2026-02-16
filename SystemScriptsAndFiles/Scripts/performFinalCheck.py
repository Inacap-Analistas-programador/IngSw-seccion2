#!/home/volbiobio/virtualenv/api/3.13/bin/python3.13_bin
# -*- coding: utf-8 -*-

import sys
import os

def perform_check():
    # Agregar el site-packages del virtualenv al path
    venv_path = '/home/volbiobio/virtualenv/api/3.13/lib/python3.13/site-packages'
    if venv_path not in sys.path:
        sys.path.insert(0, venv_path)

    os.chdir('/home/volbiobio/api')
    sys.path.insert(0, '/home/volbiobio/api')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')

    print("=" * 60)
    print("VERIFICACIÓN FINAL DE LA API")
    print("=" * 60)
    print(f"\nUsando Python: {sys.executable}")
    print(f"Versión: {sys.version}")

    try:
        import django
        django.setup()
        
        from django.conf import settings
        
        print("\n✅ Django configurado correctamente")
        print(f"   Version: {django.get_version()}")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        # Verificar base de datos
        print("\n📊 Configuración de Base de Datos:")
        print(f"   Motor: {settings.DATABASES['default']['ENGINE']}")
        print(f"   Nombre: {settings.DATABASES['default']['NAME']}")
        print(f"   Host: {settings.DATABASES['default'].get('HOST', 'localhost')}")
        print(f"   Puerto: {settings.DATABASES['default'].get('PORT', 3306)}")
        
        # Verificar aplicaciones instaladas
        print("\n📦 Apps instaladas:")
        for app in settings.INSTALLED_APPS:
            if not app.startswith('django.'):
                print(f"   - {app}")
        
        # Probar conexión a base de datos
        print("\n🔌 Probando conexión a base de datos...")
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            print("   ✅ Conexión exitosa")
        except Exception as e:
            print(f"   ❌ Error de conexión: {str(e)}")
        
        print("\n" + "=" * 60)
        print("🎉 VERIFICACIÓN COMPLETADA")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    perform_check()
