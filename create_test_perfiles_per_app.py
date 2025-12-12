#!/usr/bin/env python3
"""
Idempotent script to create test `Perfil` and `Perfil_Aplicacion` rows per `Aplicacion`.

For each Aplicacion this script creates these Perfiles (pel_descripcion):
 - "<APP> - Ninguno"        => only pea_consultar = True (others False)
 - "<APP> - Solo Crear"     => pea_consultar = True, pea_ingresar = True
 - "<APP> - Solo Modificar" => pea_consultar = True, pea_modificar = True
 - "<APP> - Solo Eliminar"  => pea_consultar = True, pea_eliminar = True
 - "<APP> - Todos"          => all pea_* = True

By default the script performs a dry-run and prints the actions it would take.
Use `--apply` to make changes in the database.

Run from repository root (script adds repo paths automatically):
  python create_test_perfiles_per_app.py --apply

"""
import os
import sys
import argparse
from pathlib import Path


def setup_django_path():
    # Ensure repo root and inner Django project are on sys.path
    repo_root = Path(__file__).resolve().parent
    # Put the Django project folder (the one that contains manage.py)
    # onto sys.path so the project package `SystemScoutsApi` can be imported
    project_dir = repo_root / 'SystemScoutsApi'
    sys.path.insert(0, str(project_dir))
    # Also keep repo root in sys.path for any top-level imports
    sys.path.insert(0, str(repo_root))
    # Change cwd to the project dir to match manage.py behaviour
    os.chdir(project_dir)
    # Use the same settings module as manage.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')


def main():
    parser = argparse.ArgumentParser(description='Create test perfiles and perfil-aplicacion rows per aplicacion')
    parser.add_argument('--apply', action='store_true', help='Write changes to the database (default: dry-run)')
    args = parser.parse_args()

    setup_django_path()

    try:
        import django
        django.setup()
    except Exception as e:
        print('Error initializing Django:', e)
        sys.exit(1)

    from ApiCoreScouts.Models.usuario_model import Perfil, Aplicacion, Perfil_Aplicacion
    from django.db import transaction

    # Define desired profile templates per application
    profile_templates = [
        ('Ninguno', {'pea_consultar': True, 'pea_ingresar': False, 'pea_modificar': False, 'pea_eliminar': False}),
        ('Solo Crear', {'pea_consultar': True, 'pea_ingresar': True, 'pea_modificar': False, 'pea_eliminar': False}),
        ('Solo Modificar', {'pea_consultar': True, 'pea_ingresar': False, 'pea_modificar': True, 'pea_eliminar': False}),
        ('Solo Eliminar', {'pea_consultar': True, 'pea_ingresar': False, 'pea_modificar': False, 'pea_eliminar': True}),
        ('Todos', {'pea_consultar': True, 'pea_ingresar': True, 'pea_modificar': True, 'pea_eliminar': True}),
    ]

    aplicacions = Aplicacion.objects.filter(apl_vigente=True).order_by('apl_descripcion')
    if not aplicacions.exists():
        print('No se encontraron aplicaciones (APLICACION). Nothing to do.')
        return

    changes = []

    for app in aplicacions:
        app_name = (app.apl_descripcion or '').strip()
        if not app_name:
            app_name = f'Aplicacion-{app.apl_id}'

        for suffix, perm_map in profile_templates:
            perfil_name = f"{app_name} - {suffix}"
            # Truncate to 50 chars to fit pel_descripcion
            if len(perfil_name) > 50:
                perfil_name = perfil_name[:47] + '...'

            perfil_obj, created = Perfil.objects.get_or_create(pel_descripcion=perfil_name, defaults={'pel_vigente': True})
            if created:
                changes.append(f"Crear Perfil: {perfil_name} (pel_id={perfil_obj.pel_id})")
            else:
                if not perfil_obj.pel_vigente:
                    changes.append(f"Activar Perfil existente: {perfil_name} (pel_id={perfil_obj.pel_id})")

            # Ensure perfil is vigente
            if perfil_obj.pel_vigente is not True:
                perfil_obj.pel_vigente = True
                if args.apply:
                    perfil_obj.save()

            # Create or update Perfil_Aplicacion
            pea, pea_created = Perfil_Aplicacion.objects.get_or_create(pel_id=perfil_obj, apl_id=app, defaults={
                'pea_consultar': perm_map['pea_consultar'],
                'pea_ingresar': perm_map['pea_ingresar'],
                'pea_modificar': perm_map['pea_modificar'],
                'pea_eliminar': perm_map['pea_eliminar'],
            })

            if pea_created:
                changes.append(f"Crear Perfil_Aplicacion: Perfil='{perfil_name}' Aplicacion='{app_name}' pea_id={pea.pea_id}")
            else:
                # Compare and update fields if needed
                updated = False
                for field, desired in perm_map.items():
                    current = getattr(pea, field)
                    if bool(current) != bool(desired):
                        changes.append(f"Actualizar Perfil_Aplicacion pea_id={pea.pea_id}: {field} {current} -> {desired}")
                        if args.apply:
                            setattr(pea, field, bool(desired))
                            updated = True
                if args.apply and updated:
                    pea.save()

    # Report changes
    if not changes:
        print('No changes required; all perfiles and perfil-aplicacion already in desired state.')
        return

    print('\nSummary of planned changes:')
    for c in changes:
        print(' -', c)

    if args.apply:
        print('\nApplied changes to the database.')
    else:
        print('\nDry-run mode (no DB writes). Use --apply to persist these changes.')


if __name__ == '__main__':
    main()
