
import os
import sys
import django
from pathlib import Path
from django.utils import timezone

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from ApiCoreScouts.Models.mantenedor_model import *
from ApiCoreScouts.Models.curso_model import *
from ApiCoreScouts.Models.persona_model import *
from ApiCoreScouts.Models.usuario_model import *

def run():
    print("Populating data...")

    # Cargo
    cargo, _ = Cargo.objects.get_or_create(car_descripcion="Guia", defaults={"car_vigente": True})
    
    # Region
    region, _ = Region.objects.get_or_create(reg_descripcion="Biobio", defaults={"reg_orden": 1, "reg_vigente": True})

    # Provincia
    provincia, _ = Provincia.objects.get_or_create(pro_descripcion="Concepcion", reg_id=region, defaults={"pro_orden": 1, "pro_vigente": True})

    # Comuna
    comuna, _ = Comuna.objects.get_or_create(com_descripcion="Concepcion", pro_id=provincia, defaults={"com_orden": 1, "com_vigente": True})

    # Tipo Curso
    tipo_curso, _ = Tipo_Curso.objects.get_or_create(tcu_descripcion="Formacion Inicial", defaults={"tcu_vigente": True})

    # Rama
    rama, _ = Rama.objects.get_or_create(ram_descripcion="Scout", defaults={"ram_edad_min": 11, "ram_edad_max": 15, "ram_vigente": True})

    # Usuario dummy for FKs
    usuario, _ = Usuario.objects.get_or_create(usu_nombre="admin", defaults={"usu_email": "admin@example.com", "password": "123", "usu_vigente": True})

    # Persona dummy for Responsable
    persona, _ = Persona.objects.get_or_create(
        per_rut="11111111-1",
        defaults={
            "usu_id": usuario,
            "per_nombre": "Admin",
            "per_apellido_paterno": "Sistema",
            "per_apellido_materno": "Scout",
            "per_fecha_nacimiento": timezone.now().date(),
            "per_email": "admin@scout.cl",
            "per_telefono": "912345678",
            "per_direccion": "Calle Falsa 123",
            "com_id": comuna,
            "per_vigente": True
        }
    )

    # Curso
    curso, created = Curso.objects.get_or_create(
        cur_codigo="CUR-001",
        defaults={
            "usu_id": usuario,
            "tcu_id": tipo_curso,
            "per_id_responsable": persona,
            "car_id_responsable": cargo,
            "com_id_lugar": comuna,
            "cur_fecha_solicitud": timezone.now(),
            "cur_descripcion": "Curso de Formacion Basica 2025",
            "cur_observacion": "Curso de prueba",
            "cur_administra": 1, # Zona
            "cur_cota_con_almuerzo": 10000,
            "cur_cota_sin_almuerzo": 5000,
            "cur_modalidad": 1, # Internado
            "cur_tipo_curso": 1, # Presencial
            "cur_lugar": "Campo Escuela",
            "cur_estado": 1, # Vigente
        }
    )
    if created:
        print(f"Created course: {curso.cur_descripcion}")
    else:
        print(f"Course already exists: {curso.cur_descripcion}")

    # Seccion
    seccion, _ = Curso_Seccion.objects.get_or_create(
        cur_id=curso,
        cus_seccion=1,
        defaults={
            "ram_id": rama,
            "cus_cant_participante": 30
        }
    )
    print(f"Seccion created/found for course {curso.cur_id}")

    print("Data population complete.")

if __name__ == "__main__":
    run()
