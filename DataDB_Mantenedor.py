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

cursor = db.cursor()

# ==== Función para insertar múltiples registros ====

def insert_many(query, data):
    cursor.executemany(query, data)
    db.commit()

# ==== MODULO 1 ROL ====

roles = []
rol_tipos = [1, 2, 3, 4, 5, 6]
for _ in range(10):
    roles.append((
        fake.job()[:50],
        random.choice(rol_tipos),
        True
    ))

insert_many(f"""
INSERT INTO {modulo}rol (ROL_DESCRIPCION, ROL_TIPO, ROL_VIGENTE)
VALUES (%s, %s, %s)
""", roles)

# ==== MODULO 2 CARGO ====

cargos = [(fake.job()[:50], True) for _ in range(10)]
insert_many(f"""
INSERT INTO {modulo}cargo (CAR_DESCRIPCION, CAR_VIGENTE)
VALUES (%s, %s)
""", cargos)

# ==== MODULO 3 RAMA ====

ramas = [(fake.word(), True) for _ in range(5)]
insert_many(f"""
INSERT INTO {modulo}rama (RAM_DESCRIPCION, RAM_VIGENTE)
VALUES (%s, %s)
""", ramas)

# ==== MODULO 4 ESTADO CIVIL ====

estados = [("Soltero", True), ("Casado", True), ("Divorciado", True), ("Viudo", True)]
insert_many(f"""
INSERT INTO {modulo}estado_civil (ESC_DESCRIPCION, ESC_VIGENTE)
VALUES (%s, %s)
""", estados)

# ==== MODULO 5 NIVEL ====

niveles = [(f"Nivel {i}", i, True) for i in range(1, 6)]
insert_many(f"""
INSERT INTO {modulo}nivel (NIV_DESCRIPCION, NIV_ORDEN, NIV_VIGENTE)
VALUES (%s, %s, %s)
""", niveles)

# ==== MODULO 6 ZONA ====

zonas = [(fake.city(), random.choice([True, False]), True) for _ in range(5)]
insert_many(f"""
INSERT INTO {modulo}zona (ZON_DESCRIPCION, ZON_UNILATERAL, ZON_VIGENTE)
VALUES (%s, %s, %s)
""", zonas)

# ==== MODULO 7 DISTRITO ====

cursor.execute(f"SELECT ZON_ID FROM {modulo}zona")
zona_ids = [z[0] for z in cursor.fetchall()]

distritos = [(random.choice(zona_ids), fake.city(), True) for _ in range(10)]
insert_many(f"""
INSERT INTO {modulo}distrito (ZON_ID, DIS_DESCRIPCION, DIS_VIGENTE)
VALUES (%s, %s, %s)
""", distritos)

# ==== MODULO 8 GRUPO ====

cursor.execute(f"SELECT DIS_ID FROM {modulo}distrito")
distrito_ids = [d[0] for d in cursor.fetchall()]

grupos = [(random.choice(distrito_ids), fake.company(), True) for _ in range(10)]
insert_many(f"""
INSERT INTO {modulo}grupo (DIS_ID, GRU_DESCRIPCION, GRU_VIGENTE)
VALUES (%s, %s, %s)
""", grupos)

# ==== MODULO 9 REGION ====

regiones = [(fake.province(), True) for _ in range(5)]
insert_many(f"""
INSERT INTO {modulo}region (REG_DESCRIPCION, REG_VIGENTE)
VALUES (%s, %s)
""", regiones)

# ==== MODULO 10 PROVINCIA ====

cursor.execute(f"SELECT REG_ID FROM {modulo}region")
region_ids = [r[0] for r in cursor.fetchall()]

provincias = [(random.choice(region_ids), fake.city(), True) for _ in range(10)]
insert_many(f"""
INSERT INTO {modulo}provincia (REG_ID, PRO_DESCRIPCION, PRO_VIGENTE)
VALUES (%s, %s, %s)
""", provincias)

# ==== MODULO 11 COMUNA ====

cursor.execute(f"SELECT PRO_ID FROM {modulo}provincia")
provincia_ids = [p[0] for p in cursor.fetchall()]

comunas = [(random.choice(provincia_ids), fake.city(), True) for _ in range(20)]
insert_many(f"""
INSERT INTO {modulo}comuna (PRO_ID, COM_DESCRIPCION, COM_VIGENTE)
VALUES (%s, %s, %s)
""", comunas)

# ==== MODULO 12 ALIMENTACION ====

tipos_ali = [1, 2]
alimentaciones = [(fake.word(), random.choice(tipos_ali), True) for _ in range(5)]
insert_many(f"""
INSERT INTO {modulo}alimentacion (ALI_DESCRIPCION, ALI_TIPO, ALI_VIGENTE)
VALUES (%s, %s, %s)
""", alimentaciones)

# ==== MODULO 13 TIPO_CURSO ====

tipos_opcion = [1, 2, 3, 4, 5, 6]

tipo_cursos = []
for _ in range(10):  # Generar 10 cursos de ejemplo
    tipo_cursos.append((
        fake.sentence(nb_words=3)[:100],   # TCU_DESCRIPCION
        random.choice(tipos_opcion),       # TCU_TIPO
        random.randint(5, 50),             # TCU_CANT_PARTICIPANTE
        random.choice([True, True, True, False])  # TCU_VIGENTE (mayor probabilidad True)
    ))

insert_many(f"""
INSERT INTO {modulo}tipo_curso (TCU_DESCRIPCION, TCU_TIPO, TCU_CANT_PARTICIPANTE, TCU_VIGENTE)
VALUES (%s, %s, %s, %s)
""", tipo_cursos)

# ==== MODULO 14 TIPO_ARCHIVO ====

tipo_archivos = []
for _ in range(10):  # Generar 10 tipos de archivo de ejemplo
    tipo_archivos.append((
        fake.word()[:50],                 # TAR_DESCRIPCION
        random.choice([True, True, True, False])  # TAR_VIGENTE
    ))

insert_many(f"""
INSERT INTO {modulo}tipo_archivo (TAR_DESCRIPCION, TAR_VIGENTE)
VALUES (%s, %s)
""", tipo_archivos)

# ==== MODULO 15 CONCEPTO_CONTABLE ====

conceptos = []
for _ in range(10):  # Crear 10 conceptos de ejemplo
    conceptos.append((
        fake.word()[:50],
        random.choice([True, True, True, False])  # COC_VIGENTE
    ))

insert_many(f"""
INSERT INTO {modulo}concepto_contable (COC_DESCRIPCION, COC_VIGENTE)
VALUES (%s, %s)
""", conceptos)

# ==== INDICADOR DE ÉXITO ====

print(f"Datos de Persona y tablas relacionadas insertados correctamente con prefijo {modulo}")

# ==== Cierre de conexión ====

cursor.close()
db.close()