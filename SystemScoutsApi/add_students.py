import os
import django
import sys
import random
from decimal import Decimal
import datetime

# Configurar Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from django.utils import timezone
from ApiCoreScouts.Models.usuario_model import Usuario
from ApiCoreScouts.Models.mantenedor_model import (
    Region, Provincia, Comuna, Rol, Estado_Civil, Nivel, Alimentacion
)
from ApiCoreScouts.Models.persona_model import (
    Persona, Persona_Curso, Persona_Estado_Curso, Persona_Individual
)
from ApiCoreScouts.Models.curso_model import (
    Curso, Curso_Seccion
)
from ApiCoreScouts.Models.pago_model import Pago_Persona

def create_students():
    print("=" * 60)
    print("AGREGANDO ESTUDIANTES AL CURSO ID 1")
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
            print("❌ No se encontró el curso con ID 1. Ejecuta populate_data.py primero.")
            return

        # Get Section 1 of Course 1
        seccion = Curso_Seccion.objects.filter(cur_id=curso).first()
        if not seccion:
            print("❌ No se encontró sección para el curso.")
            return

        # Get Basic Data
        comuna = Comuna.objects.first()
        rol = Rol.objects.get(rol_descripcion='Participante')
        estado_civil = Estado_Civil.objects.first()
        nivel = Nivel.objects.first()
        alimentacion = Alimentacion.objects.first()

        # Create 10 Students
        names = ["Maria", "Jose", "Pedro", "Ana", "Luis", "Carmen", "Francisco", "Sofia", "Jorge", "Lucia"]
        surnames = ["Gonzalez", "Munoz", "Rojas", "Diaz", "Perez", "Soto", "Contreras", "Silva", "Martinez", "Sepulveda"]

        added_count = 0

        for i in range(10):
            run_base = 30000000 + i
            run = str(run_base)
            
            # Check if exists
            if Persona.objects.filter(per_run=run).exists():
                print(f"Persona {run} ya existe, saltando...")
                continue
                
            name = names[i % len(names)]
            lastname = surnames[i % len(surnames)]
            
            # Create Persona
            persona = Persona.objects.create(
                per_run=run,
                per_dv=str(i % 10),
                per_nombres=f'{name} {i}',
                per_apelpta=lastname,
                per_mail=f'{name.lower()}{i}@scouts.cl',
                per_fecha_nac='2005-01-01',
                per_direccion='Calle Falsa 123',
                per_tipo_fono=1,
                per_vigente=True,
                esc_id=estado_civil,
                com_id=comuna,
                usu_id=admin_user,
                per_apodo=f'{name} Scout'
            )
            
            # Create Inscription (Persona_Curso)
            inscripcion = Persona_Curso.objects.create(
                per_id=persona,
                cus_id=seccion,
                rol_id=rol,
                ali_id=alimentacion,
                niv_id=nivel,
                pec_registro=True,
                pec_acreditacion=random.choice([True, False])
            )
            
            # Estado Inscripcion
            Persona_Estado_Curso.objects.create(
                usu_id=admin_user,
                pec_id=inscripcion,
                peu_estado=4 # Inscrito
            )
            
            # Create Payment (Randomly paid or pending)
            is_paid = random.choice([True, False])
            Pago_Persona.objects.create(
                per_id=persona,
                cur_id=curso,
                usu_id=admin_user,
                pap_fecha_hora=timezone.now(),
                pap_tipo=1, # Ingreso
                pap_valor=15000,
                pap_estado=1 if is_paid else 2, # 1: Pagado, 2: Pendiente
                pap_observacion='Pago ' + ('completo' if is_paid else 'pendiente')
            )
            
            added_count += 1
            print(f"✅ Agregado estudiante: {name} {lastname} ({'Pagado' if is_paid else 'Pendiente'})")

        print(f"\nTotal estudiantes agregados: {added_count}")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_students()
