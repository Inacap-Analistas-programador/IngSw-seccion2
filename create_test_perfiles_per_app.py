#!/usr/bin/env python3
"""
Idempotent script to create test `Perfil` and `Perfil_Aplicacion` rows per `Aplicacion`.

For each Aplicacion this script creates these Perfiles (PEL_DESCRIPCION):
 - "<APP> - Ninguno"        => only PEA_CONSULTAR = True (others False)
 - "<APP> - Solo Crear"     => PEA_CONSULTAR = True, PEA_INGRESAR = True
 - "<APP> - Solo Modificar" => PEA_CONSULTAR = True, PEA_MODIFICAR = True
 - "<APP> - Solo Eliminar"  => PEA_CONSULTAR = True, PEA_ELIMINAR = True
 - "<APP> - Todos"          => all PEA_* = True

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
        ('Ninguno', {'PEA_CONSULTAR': True, 'PEA_INGRESAR': False, 'PEA_MODIFICAR': False, 'PEA_ELIMINAR': False}),
        ('Solo Crear', {'PEA_CONSULTAR': True, 'PEA_INGRESAR': True, 'PEA_MODIFICAR': False, 'PEA_ELIMINAR': False}),
        ('Solo Modificar', {'PEA_CONSULTAR': True, 'PEA_INGRESAR': False, 'PEA_MODIFICAR': True, 'PEA_ELIMINAR': False}),
        ('Solo Eliminar', {'PEA_CONSULTAR': True, 'PEA_INGRESAR': False, 'PEA_MODIFICAR': False, 'PEA_ELIMINAR': True}),
        ('Todos', {'PEA_CONSULTAR': True, 'PEA_INGRESAR': True, 'PEA_MODIFICAR': True, 'PEA_ELIMINAR': True}),
    ]

    aplicacions = Aplicacion.objects.filter(APL_VIGENTE=True).order_by('APL_DESCRIPCION')
    if not aplicacions.exists():
        print('No se encontraron aplicaciones (APLICACION). Nothing to do.')
        return

    changes = []

    for app in aplicacions:
        app_name = (app.APL_DESCRIPCION or '').strip()
        if not app_name:
            app_name = f'Aplicacion-{app.APL_ID}'

        for suffix, perm_map in profile_templates:
            perfil_name = f"{app_name} - {suffix}"
            # Truncate to 50 chars to fit PEL_DESCRIPCION
            if len(perfil_name) > 50:
                perfil_name = perfil_name[:47] + '...'

            perfil_obj, created = Perfil.objects.get_or_create(PEL_DESCRIPCION=perfil_name, defaults={'PEL_VIGENTE': True})
            if created:
                changes.append(f"Crear Perfil: {perfil_name} (PEL_ID={perfil_obj.PEL_ID})")
            else:
                if not perfil_obj.PEL_VIGENTE:
                    changes.append(f"Activar Perfil existente: {perfil_name} (PEL_ID={perfil_obj.PEL_ID})")

            # Ensure perfil is vigente
            if perfil_obj.PEL_VIGENTE is not True:
                perfil_obj.PEL_VIGENTE = True
                if args.apply:
                    perfil_obj.save()

            # Create or update Perfil_Aplicacion
            pea, pea_created = Perfil_Aplicacion.objects.get_or_create(PEL_ID=perfil_obj, APL_ID=app, defaults={
                'PEA_CONSULTAR': perm_map['PEA_CONSULTAR'],
                'PEA_INGRESAR': perm_map['PEA_INGRESAR'],
                'PEA_MODIFICAR': perm_map['PEA_MODIFICAR'],
                'PEA_ELIMINAR': perm_map['PEA_ELIMINAR'],
            })

            if pea_created:
                changes.append(f"Crear Perfil_Aplicacion: Perfil='{perfil_name}' Aplicacion='{app_name}' PEA_ID={pea.PEA_ID}")
            else:
                # Compare and update fields if needed
                updated = False
                for field, desired in perm_map.items():
                    current = getattr(pea, field)
                    if bool(current) != bool(desired):
                        changes.append(f"Actualizar Perfil_Aplicacion PEA_ID={pea.PEA_ID}: {field} {current} -> {desired}")
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
