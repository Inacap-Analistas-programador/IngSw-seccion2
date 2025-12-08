"""
Script para agregar las columnas USU_IS_STAFF y USU_IS_SUPERUSER a la tabla USUARIO

INSTRUCCIONES:
1. Activar entorno virtual: venv\\Scripts\\activate
2. Ejecutar: python add_usuario_columns.py
"""
import os
import django
import sys

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from django.db import connection

def add_columns():
    print("=" * 60)
    print("AGREGANDO COLUMNAS A LA TABLA USUARIO")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        try:
            # Verificar si las columnas ya existen
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'USUARIO' 
                AND COLUMN_NAME IN ('USU_IS_STAFF', 'USU_IS_SUPERUSER')
            """)
            existing_count = cursor.fetchone()[0]
            
            if existing_count == 2:
                print("\n✅ Las columnas USU_IS_STAFF y USU_IS_SUPERUSER ya existen")
                print("\nLa base de datos está actualizada correctamente.")
                return True
            
            # Agregar USU_IS_STAFF si no existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'USUARIO' 
                AND COLUMN_NAME = 'USU_IS_STAFF'
            """)
            if cursor.fetchone()[0] == 0:
                print("\n📝 Agregando columna USU_IS_STAFF...")
                cursor.execute("""
                    ALTER TABLE USUARIO 
                    ADD COLUMN USU_IS_STAFF TINYINT(1) NOT NULL DEFAULT 0
                """)
                print("   ✅ Columna USU_IS_STAFF agregada correctamente")
            
            # Agregar USU_IS_SUPERUSER si no existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'USUARIO' 
                AND COLUMN_NAME = 'USU_IS_SUPERUSER'
            """)
            if cursor.fetchone()[0] == 0:
                print("\n📝 Agregando columna USU_IS_SUPERUSER...")
                cursor.execute("""
                    ALTER TABLE USUARIO 
                    ADD COLUMN USU_IS_SUPERUSER TINYINT(1) NOT NULL DEFAULT 0
                """)
                print("   ✅ Columna USU_IS_SUPERUSER agregada correctamente")
            
            print("\n" + "=" * 60)
            print("✅ SCRIPT COMPLETADO EXITOSAMENTE")
            print("=" * 60)
            print("\nAhora puedes iniciar el servidor con: python manage.py runserver")
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR al ejecutar el script:")
            print(f"   {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = add_columns()
    sys.exit(0 if success else 1)
