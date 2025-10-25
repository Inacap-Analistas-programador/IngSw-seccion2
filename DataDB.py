import mysql.connector
from faker import Faker
import random

fake = Faker('es_CL')

# Conexión a MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",             # cambia esto
    password="27735378Hent@i", # cambia esto
    database="ssb"
)
cursor = db.cursor()

# ---------------------
# FUNCIONES AUXILIARES
# ---------------------

def insert_many(query, data):
    cursor.executemany(query, data)
    db.commit()

# ---------------------
# TABLAS BASE
# ---------------------

# 1️⃣ ROL
roles = []
rol_tipos = [1, 2, 3, 4, 5, 6]
for _ in range(10):
    roles.append((
        fake.job(),
        random.choice(rol_tipos),
        True
    ))

insert_many("""
INSERT INTO modulomantenedores_rol (ROL_DESCRIPCION, ROL_TIPO, ROL_VIGENTE)
VALUES (%s, %s, %s)
""", roles)

# 2️⃣ CARGO
cargos = [(fake.job(), True) for _ in range(10)]
insert_many("""
INSERT INTO modulomantenedores_cargo (CAR_DESCRIPCION, CAR_VIGENTE)
VALUES (%s, %s)
""", cargos)

# 3️⃣ RAMA
ramas = [(fake.word(), True) for _ in range(5)]
insert_many("""
INSERT INTO modulomantenedores_rama (RAM_DESCRIPCION, RAM_VIGENTE)
VALUES (%s, %s)
""", ramas)

# 4️⃣ ESTADO CIVIL
estados = [("Soltero", True), ("Casado", True), ("Divorciado", True), ("Viudo", True)]
insert_many("""
INSERT INTO modulomantenedores_estado_civil (ESC_DESCRIPCION, ESC_VIGENTE)
VALUES (%s, %s)
""", estados)

# 5️⃣ NIVEL
niveles = [(f"Nivel {i}", i, True) for i in range(1, 6)]
insert_many("""
INSERT INTO modulomantenedores_nivel (NIV_DESCRIPCION, NIV_ORDEN, NIV_VIGENTE)
VALUES (%s, %s, %s)
""", niveles)

# 6️⃣ ZONA
zonas = [(fake.city(), random.choice([True, False]), True) for _ in range(5)]
insert_many("""
INSERT INTO modulomantenedores_zona (ZON_DESCRIPCION, ZON_UNILATERAL, ZON_VIGENTE)
VALUES (%s, %s, %s)
""", zonas)

# 7️⃣ DISTRITO
cursor.execute("SELECT ZON_ID FROM modulomantenedores_zona")
zona_ids = [z[0] for z in cursor.fetchall()]

distritos = [(random.choice(zona_ids), fake.city(), True) for _ in range(10)]
insert_many("""
INSERT INTO modulomantenedores_distrito (ZON_ID_id, DIS_DESCRIPCION, DIS_VIGENTE)
VALUES (%s, %s, %s)
""", distritos)

# 8️⃣ GRUPO
cursor.execute("SELECT DIS_ID FROM modulomantenedores_distrito")
distrito_ids = [d[0] for d in cursor.fetchall()]

grupos = [(random.choice(distrito_ids), fake.company(), True) for _ in range(10)]
insert_many("""
INSERT INTO modulomantenedores_grupo (DIS_ID_id, GRU_DESCRIPCION, GRU_VIGENTE)
VALUES (%s, %s, %s)
""", grupos)

# 9️⃣ REGIÓN
regiones = [(fake.state(), True) for _ in range(5)]
insert_many("""
INSERT INTO modulomantenedores_region (REG_DESCRIPCION, REG_VIGENTE)
VALUES (%s, %s)
""", regiones)

# 🔟 PROVINCIA
cursor.execute("SELECT REG_ID FROM modulomantenedores_region")
region_ids = [r[0] for r in cursor.fetchall()]

provincias = [(random.choice(region_ids), fake.city(), True) for _ in range(10)]
insert_many("""
INSERT INTO modulomantenedores_provincia (REG_ID_id, PRO_DESCRIPCION, PRO_VIGENTE)
VALUES (%s, %s, %s)
""", provincias)

# 11️⃣ COMUNA
cursor.execute("SELECT PRO_ID FROM modulomantenedores_provincia")
provincia_ids = [p[0] for p in cursor.fetchall()]

comunas = [(random.choice(provincia_ids), fake.city(), True) for _ in range(20)]
insert_many("""
INSERT INTO modulomantenedores_comuna (PRO_ID_id, COM_DESCRIPCION, COM_VIGENTE)
VALUES (%s, %s, %s)
""", comunas)

# 12️⃣ ALIMENTACIÓN
tipos_ali = [1, 2]
alimentaciones = [(fake.word(), random.choice(tipos_ali), True) for _ in range(5)]
insert_many("""
INSERT INTO modulomantenedores_alimentacion (ALI_DESCRIPCION, ALI_TIPO, ALI_VIGENTE)
VALUES (%s, %s, %s)
""", alimentaciones)

print("✅ Base de datos poblada con datos de ejemplo correctamente.")

cursor.close()
db.close()
