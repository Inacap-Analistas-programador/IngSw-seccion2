import os
import django
import random
from datetime import datetime, timezone


# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from ApiCoreScouts.Models.persona_model import *
from ApiCoreScouts.Models.curso_model import *
from ApiCoreScouts.Models.mantenedor_model import *
from ApiCoreScouts.Models.usuario_model import Usuario

def populate():
    print("Starting database population...")

    # Ensure we have at least one user
    user = Usuario.objects.first()
    if not user:
        print("Creating default user...")
        # Create a basic user if none exists (simplified)
        # Assuming you have a way to create auth user, but let's try to get one
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.exists():
             u = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        # Link to custom Usuario model if needed or just assume existing
        # This part depends on your exact Auth setup, skipping complex user creation for now
        # hoping there is at least one
        pass

    user = Usuario.objects.first()
    if not user:
        print("ERROR: No Usuario found. Please create a user first.")
        return

    # Get Catalogs
    estado_civil = Estado_Civil.objects.first() or Estado_Civil.objects.create(esc_descripcion="Soltero")
    comuna = Comuna.objects.first() # Assuming populated
    if not comuna:
        # Create minimal heavy lifting if empty
        reg = Region.objects.create(reg_descripcion="Metropolitana")
        prov = Provincia.objects.create(reg_id=reg, pro_descripcion="Santiago")
        comuna = Comuna.objects.create(pro_id=prov, com_descripcion="Santiago Centro")
    
    cargo = Cargo.objects.first() or Cargo.objects.create(car_descripcion="Responsable")
    tipo_curso = Tipo_Curso.objects.first() or Tipo_Curso.objects.create(tcu_descripcion="Inicial", tcu_tipo=1)
    rol = Rol.objects.first() or Rol.objects.create(rol_descripcion="Participante", rol_tipo=1)
    rama = Rama.objects.first() or Rama.objects.create(ram_descripcion="Golondrinas")
    alimentacion_opt = Alimentacion.objects.first() or Alimentacion.objects.create(ali_descripcion="Normal", ali_tipo=1)
    nivel = Nivel.objects.first() or Nivel.objects.create(niv_descripcion="Nivel 1", niv_orden=1)

    # Create a Course
    curso_code = f"CUR-{random.randint(1000, 9999)}"
    curso, created = Curso.objects.get_or_create(
        cur_codigo=curso_code,
        defaults={
            'usu_id': user,
            'tcu_id': tipo_curso,
            'per_id_responsable': Persona.objects.first() if Persona.objects.exists() else None, # Needs a person, chicken-egg problem. 
            # We will create a dummy responsible first if needed
            'car_id_responsable': cargo,
            'com_id_lugar': comuna,
            'cur_fecha_solicitud': datetime.now(timezone.utc),
            'cur_descripcion': f"Curso de Prueba {curso_code}",
            'cur_administra': 1,
            'cur_modalidad': 1,
            'cur_tipo_curso': 1,
            'cur_lugar': 'Campo Escuela',
            'cur_estado': 1
        }
    )
    
    # If we had no person for responsible, creating one now and updating course
    if not curso.per_id_responsable:
        resp = Persona.objects.create(
            esc_id=estado_civil, com_id=comuna, usu_id=user,
            per_run=f"{random.randint(10000000, 25000000)}", per_dv="K",
            per_apelpta="Responsable", per_nombres="Jefe", per_mail="jefe@test.com",
            per_fecha_nac=datetime(1980, 1, 1, tzinfo=timezone.utc),
            per_direccion="Calle Falsa 123", per_tipo_fono=2, per_apodo="Jefesito"
        )
        curso.per_id_responsable = resp
        curso.save()
    
    print(f"Using Course: {curso.cur_descripcion} ({curso.cur_codigo})")

    # Create Curso_Seccion
    seccion, _ = Curso_Seccion.objects.get_or_create(
        cur_id=curso, cus_seccion=1,
        defaults={'ram_id': rama, 'cus_cant_participante': 30}
    )

    # Generate Personas
    names = ["Luis", "Maria", "Jose", "Ana", "Carlos", "Paula", "Miguel", "Sofia", "Pedro", "Lucia"]
    lastnames = ["Gonzalez", "Tapia", "Perez", "Silva", "Rojas", "Soto", "Contreras", "Diaz", "Martinez", "Lopez"]
    
    for i in range(10):
        name = random.choice(names)
        lastname = random.choice(lastnames)
        run = random.randint(10000000, 25000000)
        
        # Check if exists
        if Persona.objects.filter(per_run=str(run)).exists():
            continue

        person = Persona.objects.create(
            esc_id=estado_civil,
            com_id=comuna,
            usu_id=user,
            per_run=str(run),
            per_dv=str(random.randint(0, 9)),
            per_apelpta=lastname,
            per_apelmat=random.choice(lastnames),
            per_nombres=name,
            per_mail=f"{name.lower()}.{lastname.lower()}@test.com",
            per_fecha_nac=datetime(1990 + random.randint(0, 10), 1, 1, tzinfo=timezone.utc),
            per_direccion="Direccion de prueba",
            per_tipo_fono=2,
            per_apodo=f"{name}Bot",
            per_vigente=True
        )
        print(f"Created Person: {person.per_nombres} {person.per_apelpta} (RUN: {person.per_run})")

        # Link to Course
        pc, created = Persona_Curso.objects.get_or_create(
            per_id=person,
            cus_id=seccion,
            defaults={
                'rol_id': rol,
                'ali_id': alimentacion_opt, # Assign diet
                'niv_id': nivel,
                'pec_registro': True,
                'pec_acreditacion': False, # Not accredited yet
                'pec_envio_correo_qr': True
            }
        )
        
        # Randomly assign Vehicle
        if random.choice([True, False]):
            Persona_Vehiculo.objects.create(
                pec_id=pc,
                pev_marca="Toyota",
                pev_modelo="Yaris",
                pev_patente="ABCD-12"
            )
            print(f" - Assigned Vehicle to {person.per_nombres}")

    print("Population complete.")

if __name__ == "__main__":
    populate()
