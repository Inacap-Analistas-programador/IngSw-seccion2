import mysql.connector
from faker import Faker
import random
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

fake = Faker('es_CL')
load_dotenv()

# ==== Configuración ====
modulo = ""  # cambia si usas prefijo, ej. "scouts_"

db = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD_DB"),
    database=os.getenv("DATABASE")
)
cursor = db.cursor(buffered=True)

# ==== Función genérica ====
def insert_many(query, data):
    cursor.executemany(query, data)
    db.commit()

# ==== Validar tablas base ====
tablas_base = [
    f"{modulo}usuario",
    f"{modulo}comuna",
    f"{modulo}estado_civil",
    f"{modulo}grupo",
    f"{modulo}cargo",
    f"{modulo}zona",
    f"{modulo}distrito",
    f"{modulo}nivel",
    f"{modulo}rama",
    f"{modulo}curso_seccion",
    f"{modulo}rol",
    f"{modulo}alimentacion"
]

cursor.execute("SHOW TABLES")
tablas_existentes = [t[0] for t in cursor.fetchall()]

if not all(t in tablas_existentes for t in tablas_base):
    raise Exception("❌ Faltan tablas base en la base de datos para poblar Persona y sus relaciones.")

# ==== Obtener IDs base ====
def get_ids(tabla, campo):
    cursor.execute(f"SELECT {campo} FROM {tabla}")
    return [row[0] for row in cursor.fetchall()]

usuarios = get_ids(f"{modulo}usuario", "USU_ID")
comunas = get_ids(f"{modulo}comuna", "COM_ID")
estados_civiles = get_ids(f"{modulo}estado_civil", "ESC_ID")
grupos = get_ids(f"{modulo}grupo", "GRU_ID")
cargos = get_ids(f"{modulo}cargo", "CAR_ID")
zonas = get_ids(f"{modulo}zona", "ZON_ID")
distritos = get_ids(f"{modulo}distrito", "DIS_ID")
niveles = get_ids(f"{modulo}nivel", "NIV_ID")
ramas = get_ids(f"{modulo}rama", "RAM_ID")
cursos_seccion = get_ids(f"{modulo}curso_seccion", "CUS_ID")
roles = get_ids(f"{modulo}rol", "ROL_ID")
alimentaciones = get_ids(f"{modulo}alimentacion", "ALI_ID")

# ==== POBLAR PERSONA ====
personas = []
for _ in range(50):
    run = str(fake.random_int(min=1000000, max=26000000))
    personas.append((
        random.choice(estados_civiles),
        random.choice(comunas),
        random.choice(usuarios),
        run,
        fake.random_element(elements=('0','1','2','3','4','5','6','7','8','9','K')),
        fake.last_name(),
        fake.last_name(),
        fake.first_name(),
        fake.email(),
        fake.date_of_birth(minimum_age=18, maximum_age=65),
        fake.address(),
        random.choice([1, 2, 3, 4]),
        fake.phone_number(),
        fake.word() if random.random() < 0.3 else None,
        fake.word() if random.random() < 0.3 else None,
        fake.first_name(),
        fake.phone_number(),
        fake.sentence(nb_words=4),
        random.randint(1, 9999),
        fake.job(),
        random.choice(["1 año", "2 años", "3 años", "5 años"]),
        random.choice(["1 año", "2 años", "3 años", "5 años"]),
        fake.word(),
        fake.user_name(),
        None,
        True
    ))

# Se agrega PER_FECHA_HORA con NOW() directamente en el INSERT
insert_many(f"""
INSERT INTO {modulo}persona (
    ESC_ID, COM_ID, USU_ID, PER_RUN, PER_DV, PER_APELPTA, PER_APELMAT, PER_NOMBRES, PER_MAIL,
    PER_FECHA_NAC, PER_DIRECCION, PER_TIPO_FONO, PER_FONO, PER_ALERGIA_ENFERMEDAD, PER_LIMITACION,
    PER_NOM_EMERGENCIA, PER_FONO_EMERGENCIA, PER_OTROS, PER_NUM_MMA, PER_PROFESION, PER_TIEMPO_NNAJ,
    PER_TIEMPO_ADULTO, PER_RELIGION, PER_APODO, PER_FOTO, PER_VIGENTE, PER_FECHA_HORA
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
)
""", personas)

cursor.execute(f"SELECT PER_ID FROM {modulo}persona")
persona_ids = [row[0] for row in cursor.fetchall()]

# ==== PERSONA_GRUPO ====
persona_grupo = []
for pid in persona_ids:
    persona_grupo.append((random.choice(grupos), pid, True))
insert_many(f"""
INSERT INTO {modulo}persona_grupo (GRU_ID, PER_ID, PEG_VIGENTE)
VALUES (%s, %s, %s)
""", persona_grupo)

# ==== PERSONA_FORMADOR ====
persona_formador = []
for pid in persona_ids:
    persona_formador.append((pid, random.choice([True, False]), random.choice([True, False]), random.choice([True, False]), fake.sentence(nb_words=5)))
insert_many(f"""
INSERT INTO {modulo}persona_formador (PER_ID, PEF_HAB_1, PEF_HAB_2, PEF_VERIF, PEF_HISTORIAL)
VALUES (%s, %s, %s, %s, %s)
""", persona_formador)

# ==== PERSONA_INDIVIDUAL ====
persona_individual = []
for pid in persona_ids:
    persona_individual.append((pid, random.choice(cargos), random.choice(distritos), random.choice(zonas), True))
insert_many(f"""
INSERT INTO {modulo}persona_individual (PER_ID, CAR_ID, DIS_ID, ZON_ID, PEI_VIGENTE)
VALUES (%s, %s, %s, %s, %s)
""", persona_individual)

# ==== PERSONA_NIVEL ====
persona_nivel = []
for pid in persona_ids:
    persona_nivel.append((pid, random.choice(niveles), random.choice(ramas)))
insert_many(f"""
INSERT INTO {modulo}persona_nivel (PER_ID, NIV_ID, RAM_ID)
VALUES (%s, %s, %s)
""", persona_nivel)

# ==== PERSONA_CURSO ====
cursor.execute(f"SELECT CUS_ID FROM {modulo}curso_seccion")
secciones = [row[0] for row in cursor.fetchall()]
persona_curso = []
for pid in persona_ids:
    persona_curso.append((
        pid,
        random.choice(secciones),
        random.choice(roles),
        random.choice(alimentaciones),
        random.choice(niveles),
        fake.sentence(nb_words=5),
        random.choice([True, False]),
        random.choice([True, False]),
        random.choice([True, False])
    ))
insert_many(f"""
INSERT INTO {modulo}persona_curso (PER_ID, CUS_ID, ROL_ID, ALI_ID, NIV_ID, PEC_OBSERVACION, PEC_REGISTRO, PEC_ACREDITACION, PEC_ENVIO_CORREO_QR)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""", persona_curso)

cursor.execute(f"SELECT PEC_ID FROM {modulo}persona_curso")
persona_curso_ids = [row[0] for row in cursor.fetchall()]

# ==== PERSONA_ESTADO_CURSO ====
persona_estado_curso = []
for pec in persona_curso_ids:
    persona_estado_curso.append((
        random.choice(usuarios),
        pec,
        datetime.now(),
        random.randint(1, 7),
        True
    ))
insert_many(f"""
INSERT INTO {modulo}persona_estado_curso (USU_ID, PEC_ID, PEU_FECHA_HORA, PEU_ESTADO, PEU_VIGENTE)
VALUES (%s, %s, %s, %s, %s)
""", persona_estado_curso)

# ==== PERSONA_VEHICULO ====
persona_vehiculo = []
for pec in random.sample(persona_curso_ids, min(10, len(persona_curso_ids))):
    persona_vehiculo.append((
        pec,
        fake.company(),
        fake.word().capitalize(),
        fake.bothify(text='??-####')
    ))
insert_many(f"""
INSERT INTO {modulo}persona_vehiculo (PEC_ID, PEV_MARCA, PEV_MODELO, PEV_PATENTE)
VALUES (%s, %s, %s, %s)
""", persona_vehiculo)

print("✅ Datos de personas y relaciones insertados correctamente con Faker y PER_FECHA_HORA automático")

cursor.close()
db.close()
