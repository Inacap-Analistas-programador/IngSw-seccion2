import os
import django
import sys
import random

# Configurar Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from ApiCoreScouts.Models.usuario_model import Usuario
from ApiCoreScouts.Models.mantenedor_model import (
    Rol, Cargo, Comuna, Estado_Civil, Alimentacion
)
from ApiCoreScouts.Models.persona_model import (
    Persona, Persona_Formador
)
from ApiCoreScouts.Models.curso_model import (
    Curso, Curso_Seccion, Curso_Coordinador, Curso_Formador
)

def create_staff():
    print("=" * 60)
    print("AGREGANDO STAFF (COORDINADORES Y FORMADORES) AL CURSO ID 1")
    print("=" * 60)
    
    try:
        # Get Admin User
        admin_user = Usuario.objects.filter(usu_username='admin').first()
        if not admin_user:
            print("❌ No se encontró usuario 'admin'.")
            return

        # Get Course 1
        try:
            curso = Curso.objects.get(cur_id=1)
            print(f"Curso encontrado: {curso.cur_descripcion}")
        except Curso.DoesNotExist:
            print("❌ No se encontró el curso con ID 1.")
            return

        # Get Section 1
        seccion = Curso_Seccion.objects.filter(cur_id=curso).first()
        if not seccion:
            print("❌ No se encontró sección para el curso. Creando una por defecto...")
            # Fallback create section if not exists
            # seccion = Curso_Seccion.objects.create(...)
            return

        # Ensure Roles and Cargos
        rol_formador, _ = Rol.objects.get_or_create(
            rol_descripcion='Formador',
            defaults={'rol_tipo': 2, 'rol_vigente': True}
        )
        
        cargo_coord, _ = Cargo.objects.get_or_create(
            car_descripcion='Coordinador General',
            defaults={'car_vigente': True}
        )
        
        # Basic Data
        comuna = Comuna.objects.first()
        estado_civil = Estado_Civil.objects.first()

        # Staff Data
        staff_list = [
            {"name": "Roberto", "last": "Lagos", "role": "COORD"},
            {"name": "Patricia", "last": "Vergara", "role": "COORD"},
            {"name": "Camila", "last": "Torres", "role": "FORM"},
            {"name": "Felipe", "last": "Castro", "role": "FORM"},
            {"name": "Daniela", "last": "Rios", "role": "FORM"},
        ]

        added_count = 0

        for i, data in enumerate(staff_list):
            run_base = 40000000 + i
            run = str(run_base)
            
            # Check if exists
            if Persona.objects.filter(per_run=run).exists():
                print(f"Persona {run} ({data['name']}) ya existe, saltando creación base...")
                persona = Persona.objects.get(per_run=run)
            else:
                persona = Persona.objects.create(
                    per_run=run,
                    per_dv=str(i % 10),
                    per_nombres=data['name'],
                    per_apelpta=data['last'],
                    per_mail=f"{data['name'].lower()}.{data['last'].lower()}@scouts.cl",
                    per_fecha_nac='1990-01-01',
                    per_direccion='Av. Scout 456',
                    per_tipo_fono=2,
                    per_vigente=True,
                    esc_id=estado_civil,
                    com_id=comuna,
                    usu_id=admin_user,
                    per_apodo=data['name']
                )

            # Assign Role
            if data['role'] == "COORD":
                # Check if already assigned
                if not Curso_Coordinador.objects.filter(cur_id=curso, per_id=persona).exists():
                    Curso_Coordinador.objects.create(
                        cur_id=curso,
                        per_id=persona,
                        car_id=cargo_coord,
                        cuc_cargo="Coordinador de Campo"
                    )
                    print(f"✅ Agregado coordinador: {data['name']} {data['last']}")
                    added_count += 1
                else:
                    print(f"Combinación ya existente para coordinador: {data['name']}")

            elif data['role'] == "FORM":
                # Check if already assigned
                if not Curso_Formador.objects.filter(cur_id=curso, per_id=persona).exists():
                    is_director = (data['name'] == "Camila") # Arbitrary director
                    Curso_Formador.objects.create(
                        cur_id=curso,
                        per_id=persona,
                        rol_id=rol_formador,
                        cus_id=seccion,
                        cuo_director=is_director
                    )
                    print(f"✅ Agregado formador: {data['name']} {data['last']} {'(Director)' if is_director else ''}")
                    added_count += 1
                else:
                    print(f"Combinación ya existente para formador: {data['name']}")

        print(f"\nTotal staff agregados/verificados: {len(staff_list)}")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_staff()
