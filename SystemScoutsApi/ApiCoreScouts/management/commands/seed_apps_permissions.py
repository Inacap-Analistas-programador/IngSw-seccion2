from django.core.management.base import BaseCommand
from ApiCoreScouts.Models.usuario_model import Usuario
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

MODELS_TO_PERMISSION = [
    'usuario', 'persona', 'curso', 'tipo_curso', 'pago', 
    'proveedor', 'estado_civil', 'comuna', 'provincia', 'region',
    'zona', 'distrito', 'rama', 'nivel', 'cargo', 'rol'
]

class Command(BaseCommand):
    help = "Seed: crea grupos base y asigna todos los permisos al grupo Administrador."

    def add_arguments(self, parser):
        parser.add_argument('--admin-username', default='admin', help='Username del usuario administrador (default: admin)')

    @transaction.atomic
    def handle(self, *args, **options):
        admin_username = options['admin_username']

        self.stdout.write(self.style.NOTICE('== Seed Grupos & Permisos =='))
        
        # 1. Crear el grupo Administrador
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo Administrador creado.'))
        else:
            self.stdout.write('El grupo Administrador ya existe.')

        # 2. Asignar todos los permisos de ApiCoreScouts al grupo Administrador
        all_perms = Permission.objects.filter(content_type__app_label='ApiCoreScouts')
        admin_group.permissions.set(all_perms)
        self.stdout.write(self.style.SUCCESS(f'Se asignaron {all_perms.count()} permisos al grupo Administrador.'))

        # 3. Asignar el usuario administrador al grupo
        try:
            admin_user = Usuario.objects.get(username=admin_username)
            admin_user.groups.add(admin_group)
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"Usuario '{admin_username}' añadido al grupo Administrador y marcado como superuser."))
        except Usuario.DoesNotExist:
            # Intentar conusu_username por si acaso o crear uno
            self.stdout.write(self.style.WARNING(f"Usuario '{admin_username}' no encontrado. Creando superuser..."))
            admin_user = Usuario.objects.create_superuser(
                username=admin_username,
                email='admin@example.com',
                password='adminpassword123'
            )
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{admin_username}' creado con password 'adminpassword123'."))

        self.stdout.write(self.style.SUCCESS('Seed completado con éxito.'))