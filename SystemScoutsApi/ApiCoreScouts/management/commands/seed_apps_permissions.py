from django.core.management.base import BaseCommand
from ApiCoreScouts.Models.usuario_model import Aplicacion, Perfil, Perfil_Aplicacion, Usuario
from django.db import transaction

APP_DESCRIPTIONS = [
    'Usuarios',
    'Perfiles',
    'Aplicaciones',
    'PerfilAplicacion',
    'Personas',
    'Cursos',
    'Pagos',
    'Proveedores',
    'Archivos',
    'Mantenedores',
    'AcreditacionManual',
    'VerificadorQR',
    'Pantallas2',
    'Correos'
]

class Command(BaseCommand):
    help = "Seed: crea aplicaciones base y asigna permisos al perfil del usuario admin."

    def add_arguments(self, parser):
        parser.add_argument('--admin-username', default='admin', help='Username del usuario administrador (default: admin)')
        parser.add_argument('--full', action='store_true', help='Otorga todos los permisos CRUD además de CONSULTAR.')

    @transaction.atomic
    def handle(self, *args, **options):
        admin_username = options['admin_username']
        give_all = options['full']

        self.stdout.write(self.style.NOTICE('== Seed Aplicaciones & Permisos =='))
        created_apps = []
        for desc in APP_DESCRIPTIONS:
            app_obj, created = Aplicacion.objects.get_or_create(APL_DESCRIPCION=desc, defaults={'APL_VIGENTE': True})
            if created:
                created_apps.append(desc)
        if created_apps:
            self.stdout.write(self.style.SUCCESS(f"Aplicaciones creadas: {', '.join(created_apps)}"))
        else:
            self.stdout.write('Todas las aplicaciones ya existían.')

        try:
            admin_user = Usuario.objects.get(USU_USERNAME=admin_username)
        except Usuario.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Usuario '{admin_username}' no existe."))
            return

        perfil = getattr(admin_user, 'PEL_ID', None)
        if not perfil:
            self.stdout.write(self.style.ERROR(f"Usuario '{admin_username}' no tiene perfil asignado (PEL_ID)."))
            return

        self.stdout.write(f"Perfil admin: {getattr(perfil, 'PEL_DESCRIPCION', perfil.PEL_ID)} (ID={perfil.PEL_ID})")

        for desc in APP_DESCRIPTIONS:
            app_obj = Aplicacion.objects.get(APL_DESCRIPCION=desc)
            pa, created = Perfil_Aplicacion.objects.get_or_create(
                PEL_ID=perfil,
                APL_ID=app_obj,
                defaults={
                    'PEA_CONSULTAR': True,
                    'PEA_INGRESAR': True if give_all else True,
                    'PEA_MODIFICAR': True if give_all else True,
                    'PEA_ELIMINAR': True if give_all else True,
                }
            )
            if not created and give_all:
                changed = False
                for f in ['PEA_CONSULTAR','PEA_INGRESAR','PEA_MODIFICAR','PEA_ELIMINAR']:
                    if not getattr(pa, f):
                        setattr(pa, f, True)
                        changed = True
                if changed:
                    pa.save()
            self.stdout.write(f"Permisos {'creados' if created else 'verificados'} para {desc}.")

        self.stdout.write(self.style.SUCCESS('Seed completado.'))