import mysql.connector
from faker import Faker
import random
import os
from dotenv import load_dotenv

fake = Faker('es_CL')

load_dotenv()

# ==== Configuración ====

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

# === PERFIL ====

perfiles = [(fake.job()[:50], True) for _ in range(5)]
insert_many(f"""
INSERT INTO {modulo}perfil (PEL_DESCRIPCION, PEL_VIGENTE)
VALUES (%s, %s)
""", perfiles)

cursor.execute(f"SELECT PEL_ID FROM {modulo}perfil")
perfil_ids = [row[0] for row in cursor.fetchall()]

# ==== APLICACION ====

aplicaciones = [(f"Aplicación {i}", True) for i in range(1, 6)]
insert_many(f"""
INSERT INTO {modulo}aplicacion (APL_DESCRIPCION, APL_VIGENTE)
VALUES (%s, %s)
""", aplicaciones)

cursor.execute(f"SELECT APL_ID FROM {modulo}aplicacion")
aplicacion_ids = [row[0] for row in cursor.fetchall()]

# ==== USUARIO ====

usuarios = []
for _ in range(10):
    perfil_id = random.choice(perfil_ids)
    usuarios.append((
        perfil_id,
        fake.user_name()[:100],
        fake.password(length=12),
        fake.file_path(depth=2)[:255],  # USU_RUTA_FOTO
        True
    ))

insert_many(f"""
INSERT INTO {modulo}usuario (PEL_ID, USU_USERNAME, USU_PASSWORD, USU_RUTA_FOTO, USU_VIGENTE)
VALUES (%s, %s, %s, %s, %s)
""", usuarios)

cursor.execute(f"SELECT USU_ID FROM {modulo}usuario")
usuario_ids = [row[0] for row in cursor.fetchall()]

# ==== PERFIL_APLICACION ====

perfil_aplicaciones = []
for perfil_id in perfil_ids:
    for apl_id in aplicacion_ids:
        perfil_aplicaciones.append((
            perfil_id,
            apl_id,
            random.choice([True, False]),  # PEA_INGRESAR
            random.choice([True, False]),  # PEA_MODIFICAR
            random.choice([True, False]),  # PEA_ELIMINAR
            random.choice([True, False])   # PEA_CONSULTAR
        ))

insert_many(f"""
INSERT INTO {modulo}perfil_aplicacion (
    PEL_ID, APL_ID, PEA_INGRESAR, PEA_MODIFICAR, PEA_ELIMINAR, PEA_CONSULTAR
) VALUES (%s, %s, %s, %s, %s, %s)
""", perfil_aplicaciones)

print("✅ Datos de Perfil, Aplicación, Usuario y Perfil_Aplicacion insertados correctamente")

cursor.close()
db.close()
