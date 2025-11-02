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

def insert_many(query, data):
    cursor.executemany(query, data)
    db.commit()

# =======================
# OBTENER IDS NECESARIOS
# =======================
cursor.execute(f"SELECT TAR_ID FROM {modulo}tipo_archivo")
tipo_archivo_ids = [row[0] for row in cursor.fetchall()]

cursor.execute(f"SELECT USU_ID FROM {modulo}usuario")
usuario_ids = [row[0] for row in cursor.fetchall()]

cursor.execute(f"SELECT PER_ID FROM {modulo}persona")
persona_ids = [row[0] for row in cursor.fetchall()]

cursor.execute(f"SELECT CUS_ID FROM {modulo}curso_seccion")
curso_ids = [row[0] for row in cursor.fetchall()]

# =======================
# ARCHIVO
# =======================
archivos = []
for _ in range(20):  # generar 20 archivos
    tipo_id = random.choice(tipo_archivo_ids)
    usu_crea = random.choice(usuario_ids)
    usu_modifica = random.choice(usuario_ids + [None])  # puede ser NULL
    archivos.append((
        tipo_id,
        usu_crea,
        usu_modifica,
        datetime.now(),
        fake.sentence(nb_words=5)[:100],  # ARC_DESCRIPCION
        fake.file_path(depth=3)[:255],    # ARC_RUTA
        True
    ))

insert_many(f"""
INSERT INTO {modulo}archivo (
    TAR_ID, USU_ID_CREA, USU_ID_MODIFICA, ARC_FECHA_HORA, ARC_DESCRIPCION, ARC_RUTA, ARC_VIGENTE
) VALUES (%s, %s, %s, %s, %s, %s, %s)
""", archivos)

cursor.execute(f"SELECT ARC_ID FROM {modulo}archivo")
archivo_ids = [row[0] for row in cursor.fetchall()]

# =======================
# ARCHIVO_CURSO
# =======================
archivo_curso = []
for _ in range(15):
    archivo_id = random.choice(archivo_ids)
    curso_id = random.choice(curso_ids)
    archivo_curso.append((archivo_id, curso_id))

insert_many(f"""
INSERT INTO {modulo}archivo_curso (
    ARC_ID, CUS_ID
) VALUES (%s, %s)
""", archivo_curso)

# =======================
# ARCHIVO_PERSONA
# =======================
archivo_persona = []
for _ in range(15):
    archivo_id = random.choice(archivo_ids)
    persona_id = random.choice(persona_ids)
    curso_id = random.choice(curso_ids + [None])  # puede ser NULL
    archivo_persona.append((archivo_id, persona_id, curso_id))

insert_many(f"""
INSERT INTO {modulo}archivo_persona (
    ARC_ID, PER_ID, CUS_ID
) VALUES (%s, %s, %s)
""", archivo_persona)

print("✅ Datos de Archivo, Archivo_Curso y Archivo_Persona insertados correctamente")
cursor.close()
db.close()
