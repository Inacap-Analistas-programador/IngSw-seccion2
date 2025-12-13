import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from ApiCoreScouts.Models.mantenedor_model import (
    Region, Provincia, Comuna, Estado_Civil, Alimentacion, Rol, Rama, Nivel,
    Zona, Distrito, Grupo, Cargo, Tipo_Curso
)
from ApiCoreScouts.Models.usuario_model import Usuario, Perfil
from ApiCoreScouts.Models.persona_model import Persona
from ApiCoreScouts.Models.curso_model import Curso, Tipo_Curso, Curso_Seccion
from django.utils import timezone

def run():
    print("Starting population...")

    # 1. Regiones, Provincias, Comunas
    reg, _ = Region.objects.get_or_create(reg_descripcion='Región del Biobío', defaults={'reg_vigente': True})
    prov, _ = Provincia.objects.get_or_create(pro_descripcion='Concepción', reg_id=reg, defaults={'pro_vigente': True})
    com, _ = Comuna.objects.get_or_create(com_descripcion='Concepción', pro_id=prov, defaults={'com_vigente': True})
    print(f"Location created: {com.com_descripcion}")

    # 2. Estado Civil
    estados = ['Soltero', 'Casado', 'Viudo', 'Divorciado', 'Conviviente Civil']
    for e in estados:
        Estado_Civil.objects.get_or_create(esc_descripcion=e, defaults={'esc_vigente': True})
    esc = Estado_Civil.objects.first()

    # 3. Alimentacion
    alims = ['Normal', 'Vegetariano', 'Vegano', 'Celiaco', 'Sin Lactosa']
    for i, a in enumerate(alims, 1):
        # ali_tipo choices are (1, 'Con Almuerzo'), (2, 'Sin Almuerzo') in one model, but description implies dietary preference.
        # We'll default ali_tipo=1 (Con Almuerzo) regardless of desc for now as it seems unrelated to preference text.
        Alimentacion.objects.get_or_create(ali_descripcion=a, defaults={'ali_tipo': 1, 'ali_vigente': True})

    # 4. Rol
    roles = ['Participante', 'Responsable', 'Guiadora', 'Dirigente', 'Apoderado']
    for i, r in enumerate(roles, 1):
        # rol_tipo options: 1=Participante, 2=Formadores, ... 6=Salud
        tipo = 1
        if r in ['Guiadora', 'Dirigente', 'Responsable']: tipo = 2
        Rol.objects.get_or_create(rol_descripcion=r, defaults={'rol_tipo': tipo, 'rol_vigente': True})

    # 5. Rama
    ramas = ['Lobatos', 'Golondrinas', 'Scout', 'Pioneros', 'Caminantes']
    for r in ramas:
        Rama.objects.get_or_create(ram_descripcion=r, defaults={'ram_vigente': True})
    
    # 6. Nivel
    niveles = ['Nivel 1', 'Nivel 2', 'Nivel 3']
    for i, n in enumerate(niveles, 1):
        Nivel.objects.get_or_create(niv_descripcion=n, defaults={'niv_orden': i, 'niv_vigente': True})

    # 7. Zona, Distrito, Grupo
    zona, _ = Zona.objects.get_or_create(zon_descripcion='Zona Centro', defaults={'zon_vigente': True})
    dist, _ = Distrito.objects.get_or_create(dis_descripcion='Distrito Concepción', zon_id=zona, defaults={'dis_vigente': True})
    grupo, _ = Grupo.objects.get_or_create(gru_descripcion='Grupo Guías y Scouts Concepción', dis_id=dist, defaults={'gru_vigente': True})

    # 8. Cargo
    cargos = ['Jefe de Grupo', 'Subjefe', 'Tesorero', 'Secretario', 'Responsable de Curso']
    for c in cargos:
        Cargo.objects.get_or_create(car_descripcion=c, defaults={'car_vigente': True})

    # 9. Tipo Curso
    tipos_curso = ['Inicial', 'Medio', 'Avanzado', 'Habilitación']
    for i, t in enumerate(tipos_curso, 1):
        Tipo_Curso.objects.get_or_create(tcu_descripcion=t, defaults={'tcu_tipo': 1, 'tcu_vigente': True})

    # 10. Usuario (Superuser/Admin)
    # Check if a user exists
    user = Usuario.objects.filter(usu_username='admin').first()
    if not user:
        # Create a basic profile first
        perfil, _ = Perfil.objects.get_or_create(pel_descripcion='Administrador', defaults={'pel_vigente': True})
        # Create user
        try:
            user = Usuario.objects.create_superuser(usu_username='admin', password='adminpassword', pel_id=perfil)
            print("User created: admin")
        except Exception as e:
            print(f"User creation skipped/failed: {e}")
            user = Usuario.objects.first()

    # 11. Persona (Responsable)
    if user:
        persona, created = Persona.objects.get_or_create(
            per_run='12345678',
            defaults={
                'per_dv': '9',
                'per_nombres': 'Responsable',
                'per_apelpta': 'Test',
                'per_mail': 'responsable@test.com',
                'per_fecha_nac': timezone.now(),
                'per_direccion': 'Calle Falsa 123',
                'per_tipo_fono': 2,
                'per_fono': '912345678',
                'per_apodo': 'Resp',
                'esc_id': esc,
                'com_id': com,
                'usu_id': user
            }
        )

        # 12. Curso
        tipo_curso = Tipo_Curso.objects.first()
        cargo = Cargo.objects.first()
        
        curso, created = Curso.objects.get_or_create(
            cur_codigo='CUR-001',
            defaults={
                'usu_id': user,
                'tcu_id': tipo_curso,
                'per_id_responsable': persona,
                'car_id_responsable': cargo,
                'com_id_lugar': com,
                'cur_fecha_solicitud': timezone.now(),
                'cur_descripcion': 'Curso de Prueba 2024',
                'cur_administra': 1, # Zona
                'cur_modalidad': 1, # Internado
                'cur_tipo_curso': 1, # Presencial
                'cur_lugar': 'Campo Escuela',
                'cur_estado': 1 # Vigente
            }
        )
        if created:
             print("Curso created: CUR-001")
        else:
             print("Curso exists: CUR-001")

        # 13. Curso Seccion
        rama = Rama.objects.filter(ram_descripcion='Scout').first() or Rama.objects.first()
        cs, created = Curso_Seccion.objects.get_or_create(
            cur_id=curso,
            cus_seccion=1,
            defaults={
                'ram_id': rama,
                'cus_cant_participante': 30
            }
        )
        print(f"Curso Seccion created/exists: {cs.cus_id}")

    print("Population complete.")

if __name__ == '__main__':
    run()
