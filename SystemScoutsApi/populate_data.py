import os
import django
import sys
import datetime
from decimal import Decimal

# Configurar Django
import sys
import os
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from django.utils import timezone
from ApiCoreScouts.Models.usuario_model import Usuario, Perfil
from ApiCoreScouts.Models.mantenedor_model import (
    Region, Provincia, Comuna, Zona, Distrito, Grupo, Cargo, Rol,
    Estado_Civil, Nivel, Rama, Alimentacion, Concepto_Contable, Tipo_Curso
)
from ApiCoreScouts.Models.persona_model import (
    Persona, Persona_Individual, Persona_Curso, Persona_Estado_Curso
)
from ApiCoreScouts.Models.curso_model import (
    Curso, Curso_Seccion, Curso_Fecha
)
from ApiCoreScouts.Models.pago_model import Pago_Persona

def create_test_data():
    print("=" * 60)
    print("CREANDO DATOS DE PRUEBA")
    print("=" * 60)
    
    try:
        # 0. Usuario Admin (debe existir)
        admin_user = Usuario.objects.filter(usu_username='admin').first()
        if not admin_user:
            print("❌ No se encontró usuario 'admin'. Ejecuta create_user.py primero.")
            return False

        # 1. Mantenedores Geográficos
        print("Creating Geographic Data...")
        region, _ = Region.objects.get_or_create(reg_descripcion='Biobío')
        provincia, _ = Provincia.objects.get_or_create(pro_descripcion='Concepción', reg_id=region)
        comuna, _ = Comuna.objects.get_or_create(com_descripcion='Concepción', pro_id=provincia)
        
        zona, _ = Zona.objects.get_or_create(zon_descripcion='Zona Biobío')
        distrito, _ = Distrito.objects.get_or_create(dis_descripcion='Distrito Concepción', zon_id=zona)
        grupo, _ = Grupo.objects.get_or_create(gru_descripcion='Grupo Guías y Scouts', dis_id=distrito)

        # 2. Mantenedores Básicos
        print("Creating Basic Reference Data...")
        cargo, _ = Cargo.objects.get_or_create(car_descripcion='Responsable de Curso')
        rol, _ = Rol.objects.get_or_create(rol_descripcion='Participante', rol_tipo=1)
        estado_civil, _ = Estado_Civil.objects.get_or_create(esc_descripcion='Soltero/a')
        nivel, _ = Nivel.objects.get_or_create(niv_descripcion='Nivel Medio', niv_orden=2)
        rama, _ = Rama.objects.get_or_create(ram_descripcion='Tropa')
        alimentacion, _ = Alimentacion.objects.get_or_create(ali_descripcion='Normal', ali_tipo=1)
        concepto, _ = Concepto_Contable.objects.get_or_create(coc_descripcion='Pago Curso')
        tipo_curso, _ = Tipo_Curso.objects.get_or_create(tcu_descripcion='Curso Básico', tcu_tipo=1)

        # 3. Personas
        print("Creating Personas...")
        # Responsable del Curso
        responsable, created = Persona.objects.get_or_create(
            per_run='11111111',
            defaults={
                'per_dv': '1', 'per_nombres': 'Responsable', 'per_apelpta': 'Principal', 'per_mail': 'resp@scouts.cl',
                'per_fecha_nac': '1980-01-01', 'per_direccion': 'Calle 123', 'per_tipo_fono': 2, 
                'per_vigente': True, 'esc_id': estado_civil, 'com_id': comuna, 'usu_id': admin_user,
                'per_apodo': 'Jefe'
            }
        )

        # Participante
        participante, created = Persona.objects.get_or_create(
            per_run='22222222',
            defaults={
                'per_dv': '2', 'per_nombres': 'Juan', 'per_apelpta': 'Pérez', 'per_mail': 'juan@scouts.cl',
                'per_fecha_nac': '2000-05-15', 'per_direccion': 'Avenida 456', 'per_tipo_fono': 2,
                'per_vigente': True, 'esc_id': estado_civil, 'com_id': comuna, 'usu_id': admin_user,
                'per_apodo': 'Juancho'
            }
        )
        
        # Datos extra participante
        Persona_Individual.objects.get_or_create(
            per_id=participante,
            defaults={'car_id': cargo, 'dis_id': distrito, 'zon_id': zona}
        )

        # 4. Curso
        print("Creating Curso...")
        curso, created = Curso.objects.get_or_create(
            cur_codigo='CUR-2025-01',
            defaults={
                'usu_id': admin_user,
                'tcu_id': tipo_curso,
                'per_id_responsable': responsable,
                'car_id_responsable': cargo,
                'com_id_lugar': comuna,
                'cur_fecha_solicitud': timezone.now(),
                'cur_descripcion': 'Curso de Formación Inicial',
                'cur_administra': 1, # Zona
                'cur_cota_con_almuerzo': 15000,
                'cur_cota_sin_almuerzo': 10000,
                'cur_modalidad': 1, # Internado
                'cur_tipo_curso': 1, # Presencial
                'cur_lugar': 'Campo Escuela',
                'cur_estado': 1 # Vigente
            }
        )
        
        # Fecha del curso
        Curso_Fecha.objects.get_or_create(
            cur_id=curso,
            defaults={
                'cuf_fecha_inicio': timezone.now() + datetime.timedelta(days=10),
                'cuf_fecha_termino': timezone.now() + datetime.timedelta(days=12),
                'cuf_tipo': 1
            }
        )
        
        # Seccion
        seccion, _ = Curso_Seccion.objects.get_or_create(
            cur_id=curso,
            cus_seccion=1,
            defaults={'ram_id': rama, 'cus_cant_participante': 30}
        )

        # 5. Inscripcion
        print("Creating Inscripcion...")
        inscripcion, created = Persona_Curso.objects.get_or_create(
            per_id=participante,
            cus_id=seccion,
            defaults={
                'rol_id': rol,
                'ali_id': alimentacion,
                'niv_id': nivel,
                'pec_registro': True,
                'pec_acreditacion': True
            }
        )
        
        # Estado Inscripcion
        Persona_Estado_Curso.objects.create(
            usu_id=admin_user,
            pec_id=inscripcion,
            peu_estado=4 # Inscrito
        )

        # 6. Pago
        print("Creating Pago...")
        Pago_Persona.objects.get_or_create(
            per_id=participante,
            cur_id=curso,
            defaults={
                'usu_id': admin_user,
                'pap_fecha_hora': timezone.now(),
                'pap_tipo': 1, # Ingreso
                'pap_valor': 15000,
                'pap_estado': 1, # Pagado
                'pap_observacion': 'Pago completo'
            }
        )

        print("\n" + "="*60)
        print("✅ DATOS DE PRUEBA CREADOS CORRECTAMENTE")
        print("="*60)
        return True

    except Exception as e:
        print(f"\n❌ ERROR al crear datos de prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    create_test_data()
