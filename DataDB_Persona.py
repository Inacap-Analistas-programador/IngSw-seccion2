import mysql.connector
from faker import Faker
import random

fake = Faker('es_CL')
# ==== Variable const de los Modulos ====

modulo = ""
password_db = ""

# ==== Conexión a la base de datos ====

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",             # cambia esto
    password=password_db,
    database="ssb"
)

cursor = db.cursor()

# ==== Función para insertar múltiples registros ====

def insert_many(query, data):
    cursor.executemany(query, data)
    db.commit()

# ====== PERSONA ======
personas = []
for _ in range(10):
    run = fake.random_int(min=10000000, max=25000000)
    dv = str(random.randint(0, 9))
    personas.append((
        1,                          # ESC_ID ejemplo
        1,                          # COM_ID ejemplo
        1,                          # USU_ID ejemplo
        fake.date_of_birth(minimum_age=18, maximum_age=65),  # PER_FECHA_NAC
        str(run),                   # PER_RUN
        dv,                         # PER_DV
        fake.last_name()[:50],      # PER_APELPTA
        fake.last_name()[:50],      # PER_APELMAT
        fake.first_name()[:50],     # PER_NOMBRES
        fake.email()[:100],         # PER_MAIL
        fake.address()[:255],       # PER_DIRECCION
        random.randint(1, 4),       # PER_TIPO_FONO
        fake.phone_number()[:15],   # PER_FONO
        None,                       # PER_ALERGIA_ENFERMEDAD
        None,                       # PER_LIMITACION
        None,                       # PER_NOM_EMERGENCIA
        None,                       # PER_FONO_EMERGENCIA
        None,                       # PER_OTROS
        None,                       # PER_NUM_MMA
        None,                       # PER_PROFESION
        None,                       # PER_TIEMPO_NNAJ
        None,                       # PER_TIEMPO_ADULTO
        None,                       # PER_RELIGION
        fake.first_name()[:50],     # PER_APODO
        None,                       # PER_FOTO
        True                        # PER_VIGENTE
    ))

insert_many(f"""
INSERT INTO {modulo}_persona (
    ESC_ID, COM_ID, USU_ID, PER_FECHA_NAC, PER_RUN, PER_DV, PER_APELPTA, PER_APELMAT, PER_NOMBRES,
    PER_MAIL, PER_DIRECCION, PER_TIPO_FONO, PER_FONO, PER_ALERGIA_ENFERMEDAD, PER_LIMITACION,
    PER_NOM_EMERGENCIA, PER_FONO_EMERGENCIA, PER_OTROS, PER_NUM_MMA, PER_PROFESION, PER_TIEMPO_NNAJ,
    PER_TIEMPO_ADULTO, PER_RELIGION, PER_APODO, PER_FOTO, PER_VIGENTE
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", personas)

# Obtenemos IDs de las personas insertadas
cursor.execute(f"SELECT PER_ID FROM {modulo}_persona ORDER BY PER_ID DESC LIMIT 10")
persona_ids = [row[0] for row in cursor.fetchall()]

# ====== PERSONA_GRUPO ======
persona_grupo = [(1, pid, True) for pid in persona_ids]  # GRU_ID=1 ejemplo
insert_many(f"""
INSERT INTO {modulo}_persona_grupo (GRU_ID, PER_ID, PEG_VIGENTE)
VALUES (%s, %s, %s)
""", persona_grupo)

# ====== PERSONA_FORMADOR ======
persona_formador = [(pid, random.choice([True, False]), random.choice([True, False]), False, None) for pid in persona_ids]
insert_many(f"""
INSERT INTO {modulo}_persona_formador (PER_ID, PEF_HAB_1, PEF_HAB_2, PEF_VERIF, PEF_HISTORIAL)
VALUES (%s, %s, %s, %s, %s)
""", persona_formador)

# ====== PERSONA_INDIVIDUAL ======
persona_individual = [(pid, 1, 1, None, True) for pid in persona_ids]  # CAR_ID=1, DIS_ID=1 ejemplo
insert_many(f"""
INSERT INTO {modulo}_persona_individual (PER_ID, CAR_ID, DIS_ID, ZON_ID, PEI_VIGENTE)
VALUES (%s, %s, %s, %s, %s)
""", persona_individual)

# ====== PERSONA_NIVEL ======
persona_nivel = [(pid, 1, 1, 1) for pid in persona_ids]  # NIV_ID=1, RAM_ID=1 ejemplo
insert_many(f"""
INSERT INTO {modulo}_persona_nivel (PER_ID, NIV_ID, RAM_ID)
VALUES (%s, %s, %s, %s)
""", persona_nivel)

# ====== PERSONA_CURSO ======
persona_curso = [(pid, 1, 1, None, None, None, False, False) for pid in persona_ids]  # CUS_ID=1, ROL_ID=1
insert_many(f"""
INSERT INTO {modulo}_persona_curso (PER_ID, CUS_ID, ROL_ID, ALI_ID, NIV_ID, PEC_OBSERVACION, PEC_REGISTRO, PEC_ACREDITACION)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", persona_curso)

# Obtenemos IDs de los cursos insertados
cursor.execute(f"SELECT PEC_ID FROM {modulo}_persona_curso ORDER BY PEC_ID DESC LIMIT 10")
curso_ids = [row[0] for row in cursor.fetchall()]

# ====== PERSONA_ESTADO_CURSO ======
persona_estado_curso = [(1, cid, fake.date_time_this_year(), random.randint(1, 7), True) for cid in curso_ids]  # USU_ID=1 ejemplo
insert_many(f"""
INSERT INTO {modulo}_persona_estado_curso (USU_ID, PEC_ID, PEU_FECHA_HORA, PEU_ESTADO, PEU_VIGENTE)
VALUES (%s, %s, %s, %s, %s)
""", persona_estado_curso)

# ====== PERSONA_VEHICULO ======
persona_vehiculo = [(cid, fake.company()[:50], fake.word()[:50], fake.bothify(text='??##??')) for cid in curso_ids]
insert_many(f"""
INSERT INTO {modulo}_persona_vehiculo (PEC_ID, PEV_MARCA, PEV_MODELO, PEV_PATENTE)
VALUES (%s, %s, %s, %s)
""", persona_vehiculo)

print(f"Datos de Persona y tablas relacionadas insertados correctamente con prefijo {modulo}")