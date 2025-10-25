import mysql.connector
from faker import Faker
import random

fake = Faker('es_CL')
# ==== Variable const de los Modulos ====

modulo = "modulomantenedores"
password_db = "27735378Hent@i"

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
INSERT INTO {modulo}_rol (ROL_DESCRIPCION, ROL_TIPO, ROL_VIGENTE)
VALUES (%s, %s, %s)
""", roles)

# ==== MODULO 2 CARGO ====

cargos = [(fake.job()[:50], True) for _ in range(10)]
insert_many(f"""
INSERT INTO {modulo}_cargo (CAR_DESCRIPCION, CAR_VIGENTE)
VALUES (%s, %s)
""", cargos)

# ==== MODULO 3 RAMA ====

ramas = [(fake.word(), True) for _ in range(5)]
insert_many(f"""
INSERT INTO {modulo}_rama (RAM_DESCRIPCION, RAM_VIGENTE)
VALUES (%s, %s)
""", ramas)

# ==== MODULO 4 ESTADO CIVIL ====

estados = [("Soltero", True), ("Casado", True), ("Divorciado", True), ("Viudo", True)]
insert_many(f"""
INSERT INTO {modulo}_estado_civil (ESC_DESCRIPCION, ESC_VIGENTE)
VALUES (%s, %s)
""", estados)

# ==== MODULO 5 NIVEL ====

niveles = [(f"Nivel {i}", i, True) for i in range(1, 6)]
insert_many(f"""
INSERT INTO {modulo}_nivel (NIV_DESCRIPCION, NIV_ORDEN, NIV_VIGENTE)
VALUES (%s, %s, %s)
""", niveles)

# ==== MODULO 6 ZONA ====

zonas = [(fake.city(), random.choice([True, False]), True) for _ in range(5)]
insert_many(f"""
INSERT INTO {modulo}_zona (ZON_DESCRIPCION, ZON_UNILATERAL, ZON_VIGENTE)
VALUES (%s, %s, %s)
""", zonas)

# ==== MODULO 7 DISTRITO ====

cursor.execute(f"SELECT ZON_ID FROM {modulo}_zona")
zona_ids = [z[0] for z in cursor.fetchall()]

distritos = [(random.choice(zona_ids), fake.city(), True) for _ in range(10)]
insert_many(f"""
INSERT INTO {modulo}_distrito (ZON_ID_id, DIS_DESCRIPCION, DIS_VIGENTE)
VALUES (%s, %s, %s)
""", distritos)

# ==== MODULO 8 GRUPO ====

cursor.execute(f"SELECT DIS_ID FROM {modulo}_distrito")
distrito_ids = [d[0] for d in cursor.fetchall()]

grupos = [(random.choice(distrito_ids), fake.company(), True) for _ in range(10)]
insert_many(f"""
INSERT INTO {modulo}_grupo (DIS_ID_id, GRU_DESCRIPCION, GRU_VIGENTE)
VALUES (%s, %s, %s)
""", grupos)

# ==== MODULO 9 REGION ====

regiones = [(fake.province(), True) for _ in range(5)]
insert_many(f"""
INSERT INTO {modulo}_region (REG_DESCRIPCION, REG_VIGENTE)
VALUES (%s, %s)
""", regiones)

# ==== MODULO 10 PROVINCIA ====

cursor.execute(f"SELECT REG_ID FROM {modulo}_region")
region_ids = [r[0] for r in cursor.fetchall()]

provincias = [(random.choice(region_ids), fake.city(), True) for _ in range(10)]
insert_many(f"""
INSERT INTO {modulo}_provincia (REG_ID_id, PRO_DESCRIPCION, PRO_VIGENTE)
VALUES (%s, %s, %s)
""", provincias)

# ==== MODULO 11 COMUNA ====

cursor.execute(f"SELECT PRO_ID FROM {modulo}_provincia")
provincia_ids = [p[0] for p in cursor.fetchall()]

comunas = [(random.choice(provincia_ids), fake.city(), True) for _ in range(20)]
insert_many(f"""
INSERT INTO {modulo}_comuna (PRO_ID_id, COM_DESCRIPCION, COM_VIGENTE)
VALUES (%s, %s, %s)
""", comunas)

# ==== MODULO 12 ALIMENTACION ====

tipos_ali = [1, 2]
alimentaciones = [(fake.word(), random.choice(tipos_ali), True) for _ in range(5)]
insert_many(f"""
INSERT INTO {modulo}_alimentacion (ALI_DESCRIPCION, ALI_TIPO, ALI_VIGENTE)
VALUES (%s, %s, %s)
""", alimentaciones)

# ==== INDICADOR DE ÉXITO ====

print(f"Datos de Persona y tablas relacionadas insertados correctamente con prefijo {modulo}")

# ==== Cierre de conexión ====

cursor.close()
db.close()
