"""
Script para resetear la contraseña del usuario admin

INSTRUCCIONES:
1. Activar entorno virtual: venv\\Scripts\\activate
2. Ejecutar: python reset_admin_password.py
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from ApiCoreScouts.Models.usuario_model import Usuario

def reset_admin_password():
    print("=" * 60)
    print("RESETEAR CONTRASEÑA DEL USUARIO ADMIN")
    print("=" * 60)
    
    try:
        # Buscar el usuario admin
        usuario = Usuario.objects.get(USU_USERNAME='admin')
        print(f"\n✅ Usuario encontrado: {usuario.USU_USERNAME}")
        print(f"   ID: {usuario.USU_ID}")
        print(f"   Vigente: {usuario.USU_VIGENTE}")
        
        # Cambiar contraseña usando el método correcto
        usuario.set_password('admin')
        usuario.save()
        
        print("\n" + "=" * 60)
        print("✅ CONTRASEÑA ACTUALIZADA EXITOSAMENTE")
        print("=" * 60)
        print("\nCredenciales de acceso:")
        print("   Usuario: admin")
        print("   Contraseña: admin")
        print("\nAhora puedes iniciar sesión en el sistema.")
        
        return True
        
    except Usuario.DoesNotExist:
        print("\n❌ ERROR: El usuario 'admin' no existe en la base de datos")
        print("\nDebes crear el usuario primero usando:")
        print("   python manage.py createsuperuser")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR al resetear contraseña:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = reset_admin_password()
    sys.exit(0 if success else 1)
