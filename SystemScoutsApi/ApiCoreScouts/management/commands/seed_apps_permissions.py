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
            app_obj, created = Aplicacion.objects.get_or_create(apl_descripcion=desc, defaults={'apl_vigente': True})
            if created:
                created_apps.append(desc)
        if created_apps:
            self.stdout.write(self.style.SUCCESS(f"Aplicaciones creadas: {', '.join(created_apps)}"))
        else:
            self.stdout.write('Todas las aplicaciones ya existían.')

        try:
            admin_user = Usuario.objects.get(usu_username=admin_username)
        except Usuario.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Usuario '{admin_username}' no existe."))
            return

        perfil = getattr(admin_user, 'pel_id', None)
        if not perfil:
            self.stdout.write(self.style.ERROR(f"Usuario '{admin_username}' no tiene perfil asignado (pel_id)."))
            return

        self.stdout.write(f"Perfil admin: {getattr(perfil, 'pel_descripcion', perfil.pel_id)} (ID={perfil.pel_id})")

        for desc in APP_DESCRIPTIONS:
            app_obj = Aplicacion.objects.get(apl_descripcion=desc)
            pa, created = Perfil_Aplicacion.objects.get_or_create(
                pel_id=perfil,
                apl_id=app_obj,
                defaults={
                    'pea_consultar': True,
                    'pea_ingresar': True if give_all else True,
                    'pea_modificar': True if give_all else True,
                    'pea_eliminar': True if give_all else True,
                }
            )
            if not created and give_all:
                changed = False
                for f in ['pea_consultar','pea_ingresar','pea_modificar','pea_eliminar']:
                    if not getattr(pa, f):
                        setattr(pa, f, True)
                        changed = True
                if changed:
                    pa.save()
            self.stdout.write(f"Permisos {'creados' if created else 'verificados'} para {desc}.")

        self.stdout.write(self.style.SUCCESS('Seed completado.'))