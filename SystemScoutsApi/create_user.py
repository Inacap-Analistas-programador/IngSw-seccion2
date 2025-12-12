import os
import django
import sys

# Configurar Django
import sys
import os

# Agrega el directorio actual al path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from ApiCoreScouts.Models.usuario_model import Usuario, Perfil

def create_admin_user():
    username = 'admin'
    password = 'admin123'  # Contraseña segura para desarrollo
    
    print(f"Creating user '{username}'...")
    
    try:
        # Asegurar que existe el perfil Administrador
        perfil, created = Perfil.objects.get_or_create(
            pel_descripcion='Administrador',
            defaults={'pel_vigente': True}
        )
        if created:
            print(f"Created profile 'Administrador'")
        
        # Verificar si el usuario ya existe
        if Usuario.objects.filter(usu_username=username).exists():
            print(f"User '{username}' already exists. Updating password...")
            user = Usuario.objects.get(usu_username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.pel_id = perfil
            user.usu_vigente = True
            user.save()
            print(f"User '{username}' updated successfully.")
        else:
            # Crear nuevo usuario
            user = Usuario.objects.create_user(
                usu_username=username,
                password=password,
                pel_id=perfil,
                is_staff=True,
                is_superuser=True,
                usu_vigente=True
            )
            print(f"User '{username}' created successfully.")
            
        print("\n" + "="*40)
        print(f"✅ USER CREATED/UPDATED")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print("="*40)
        return True
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    create_admin_user()
