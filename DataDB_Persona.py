import mysql.connector
from faker import Faker
import random
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

fake = Faker('es_CL')

load_dotenv()

# ==== Configuración ====

modulo = ""

db = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    database = os.getenv("DATABASE")
)
cursor = db.cursor(buffered=True)

# ==== Función para insertar múltiples registros ====
def insert_many(query, data):
    cursor.executemany(query, data)
    db.commit()

# ==== Validar tablas base ====
tablas_base = [
    f"{modulo}usuario",
    f"{modulo}persona",
    f"{modulo}rol",
    f"{modulo}cargo",
    f"{modulo}comuna",
    f"{modulo}tipo_curso",
    f"{modulo}alimentacion",
    f"{modulo}rama",
]

cursor.execute("SHOW TABLES")
tablas_existentes = [t[0] for t in cursor.fetchall()]

if not all(t in tablas_existentes for t in tablas_base):
    raise Exception("Faltan tablas base en la base de datos.")

# ==== Obtener IDs base ====
def get_ids(tabla, campo):
    cursor.execute(f"SELECT {campo} FROM {tabla}")
    return [row[0] for row in cursor.fetchall()]

usuarios = get_ids(f"{modulo}usuario", "USU_ID")
personas = get_ids(f"{modulo}persona", "PER_ID")
roles = get_ids(f"{modulo}rol", "ROL_ID")
cargos = get_ids(f"{modulo}cargo", "CAR_ID")
comunas = get_ids(f"{modulo}comuna", "COM_ID")
tipos_curso = get_ids(f"{modulo}tipo_curso", "TCU_ID")
alimentaciones = get_ids(f"{modulo}alimentacion", "ALI_ID")
ramas = get_ids(f"{modulo}rama", "RAM_ID")

if not (usuarios and personas and roles and cargos and comunas and tipos_curso and alimentaciones and ramas):
    raise Exception("Faltan registros base en una o más tablas relacionadas.")

# ==== CURSO ====
cursos = []
for _ in range(10):
    cursos.append((
        random.choice(usuarios),
        random.choice(tipos_curso),
        random.choice(personas),
        random.choice(cargos),
        random.choice(comunas),
        datetime.now(),
        fake.date_this_year(),
        fake.bothify(text='CUR-####'),
        fake.sentence(nb_words=4),
        fake.sentence(nb_words=6),
        random.choice([1, 2]),  # CUR_ADMINISTRA
        random.randint(10000, 30000),  # COTA CON ALMUERZO
        random.randint(5000, 15000),   # COTA SIN ALMUERZO
        random.choice([1, 2, 3]),  # MODALIDAD
        random.choice([1, 2, 3]),  # TIPO CURSO
        fake.city(),
        random.choice([0, 1, 2, 3])  # ESTADO
    ))

insert_many(f"""
INSERT INTO {modulo}curso (
    USU_ID, TCU_ID, PER_ID_RESPONSABLE, CAR_ID_RESPONSABLE, COM_ID_LUGAR,
    CUR_FECHA_HORA, CUR_FECHA_SOLICITUD, CUR_CODIGO, CUR_DESCRIPCION, CUR_OBSERVACION,
    CUR_ADMINISTRA, CUR_COTA_CON_ALMUERZO, CUR_COTA_SIN_ALMUERZO, CUR_MODALIDAD,
    CUR_TIPO_CURSO, CUR_LUGAR, CUR_ESTADO
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", cursos)

cursor.execute(f"SELECT CUR_ID FROM {modulo}curso")
curso_ids = [row[0] for row in cursor.fetchall()]

# ==== CURSO_CUOTA ====
cuotas = []
for cid in curso_ids:
    cuotas.append((cid, 1, fake.date_this_year(), random.uniform(10000, 30000)))
    cuotas.append((cid, 2, fake.date_this_year(), random.uniform(5000, 15000)))

insert_many(f"""
INSERT INTO {modulo}curso_cuota (CUR_ID, CUU_TIPO, CUU_FECHA, CUU_VALOR)
VALUES (%s, %s, %s, %s)
""", cuotas)

# ==== CURSO_FECHA ====
fechas = []
for cid in curso_ids:
    inicio = fake.date_this_year()
    termino = inicio + timedelta(days=random.randint(3, 10))
    fechas.append((cid, inicio, termino, random.choice([1, 2, 3])))

insert_many(f"""
INSERT INTO {modulo}curso_fecha (CUR_ID, CUF_FECHA_INICIO, CUF_FECHA_TERMINO, CUF_TIPO)
VALUES (%s, %s, %s, %s)
""", fechas)

# ==== CURSO_ALIMENTACION ====
alimentacion_data = []
for cid in curso_ids:
    for _ in range(3):
        alimentacion_data.append((
            cid,
            random.choice(alimentaciones),
            fake.date_this_year(),
            random.choice([1, 2, 3, 4, 5]),
            fake.word(),
            random.randint(0, 10),
            True
        ))

insert_many(f"""
INSERT INTO {modulo}curso_alimentacion (CUR_ID, ALI_ID, CUA_FECHA, CUA_TIEMPO, CUA_DESCRIPCION, CUA_CANTIDAD_ADICIONAL, CUA_VIGENTE)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""", alimentacion_data)

# ==== CURSO_COORDINADOR ====
coordinadores = []
for cid in curso_ids:
    for _ in range(2):
        coordinadores.append((
            cid,
            random.choice(personas),
            random.choice(cargos),
            fake.job()
        ))

insert_many(f"""
INSERT INTO {modulo}curso_coordinador (CUR_ID, PER_ID, CAR_ID, CUC_CARGO)
VALUES (%s, %s, %s, %s)
""", coordinadores)

# ==== CURSO_SECCION ====
secciones = []
for cid in curso_ids:
    for _ in range(random.randint(1, 3)):
        secciones.append((
            cid,
            random.choice(ramas),
            random.randint(1, 5),
            random.randint(10, 30)
        ))

insert_many(f"""
INSERT INTO {modulo}curso_seccion (CUR_ID, RAM_ID, CUS_SECCION, CUS_CANT_PARTICIPANTE)
VALUES (%s, %s, %s, %s)
""", secciones)

cursor.execute(f"SELECT CUS_ID FROM {modulo}curso_seccion")
seccion_ids = [row[0] for row in cursor.fetchall()]

# ==== CURSO_FORMADOR ====
formadores = []
for cid in curso_ids:
    for _ in range(3):
        formadores.append((
            cid,
            random.choice(personas),
            random.choice(roles),
            random.choice(seccion_ids),
            random.choice([True, False])
        ))

insert_many(f"""
INSERT INTO {modulo}curso_formador (CUR_ID, PER_ID, ROL_ID, CUS_ID, CUO_DIRECTOR)
VALUES (%s, %s, %s, %s, %s)
""", formadores)

print("✅ Datos de cursos insertados correctamente con Faker")

cursor.close()
db.close()
