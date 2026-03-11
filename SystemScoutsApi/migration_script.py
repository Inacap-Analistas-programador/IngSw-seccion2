
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ApiCoreScouts.Models.usuario_model import Perfil, Aplicacion, Perfil_Aplicacion, Usuario as OldUsuario

# Mapping from apl_descripcion to (app_label, model_name)
# This needs to be populated based on the actual applications defined in the DB
APP_MODEL_MAPPING = {
    'Usuarios': ('ApiCoreScouts', 'usuario'),
    'Personas': ('ApiCoreScouts', 'persona'),
    'Cursos': ('ApiCoreScouts', 'curso_seccion'),
    'Pagos': ('ApiCoreScouts', 'pago'),
    'Mantenedores': ('ApiCoreScouts', 'estado_civil'), # Example, may need refinement
}

def migrate_data():
    print("Iniciando migración de datos...")

    # 1. Migrar Perfiles a Grupos
    for perfil in Perfil.objects.all():
        group, created = Group.objects.get_or_create(name=perfil.pel_descripcion)
        if created:
            print(f"Grupo creado: {group.name}")
        
        # 2. Migrar Permisos del Perfil
        for pa in Perfil_Aplicacion.objects.filter(pel_id=perfil):
            app_desc = pa.apl_id.apl_descripcion
            if app_desc in APP_MODEL_MAPPING:
                app_label, model_name = APP_MODEL_MAPPING[app_desc]
                try:
                    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                    
                    # Mapping boolean flags to Django codenames
                    perm_map = {
                        'pea_consultar': f'view_{model_name}',
                        'pea_ingresar': f'add_{model_name}',
                        'pea_modificar': f'change_{model_name}',
                        'pea_eliminar': f'delete_{model_name}',
                    }
                    
                    for old_flag, new_codename in perm_map.items():
                        if getattr(pa, old_flag):
                            permission = Permission.objects.get(codename=new_codename, content_type=content_type)
                            group.permissions.add(permission)
                            print(f"  Permiso añadido a {group.name}: {new_codename}")
                except ContentType.DoesNotExist:
                    print(f"  Error: ContentType no encontrado para {app_label}.{model_name}")
                except Permission.DoesNotExist:
                    print(f"  Error: Permiso {new_codename} no encontrado.")

    # 3. Asignar Usuarios a Grupos
    # Nota: El modelo Usuario se refactorizará para heredar de AbstractUser.
    # Tras la refactorización, los usuarios mantendrán su relación con el perfil (ahora grupo).
    # Este script asume que la refactorización de modelos ya ocurrió o ocurrirá pronto.
    print("Migración finalizada.")

if __name__ == "__main__":
    migrate_data()
