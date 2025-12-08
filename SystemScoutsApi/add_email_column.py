"""
Script para agregar la columna usu_email a la tabla USUARIO
"""
import os
import django
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from django.db import connection

def add_email_column():
    print("=" * 60)
    print("AGREGANDO COLUMNA usu_email A LA TABLA USUARIO")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        try:
            # Verificar si la columna ya existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'usuario' 
                AND COLUMN_NAME = 'usu_email'
            """)
            exists = cursor.fetchone()[0]
            
            if exists:
                print("\n✅ La columna usu_email ya existe")
                return True
            
            print("\n📝 Agregando columna usu_email...")
            cursor.execute("""
                ALTER TABLE usuario 
                ADD COLUMN usu_email VARCHAR(255) NULL
            """)
            print("   ✅ Columna usu_email agregada correctamente")
            
            print("\n" + "=" * 60)
            print("✅ SCRIPT COMPLETADO EXITOSAMENTE")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR al ejecutar el script:")
            print(f"   {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = add_email_column()
    sys.exit(0 if success else 1)
