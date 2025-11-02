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

# ==== PROVEEDORES ====

proveedores = []
for _ in range(10):
    proveedores.append((
        fake.company()[:100],
        fake.phone_number()[:15],
        fake.phone_number()[:15] if random.choice([True, False]) else None,
        fake.address()[:100],
        fake.sentence(nb_words=10)[:500],
        True
    ))

insert_many(f"""
INSERT INTO {modulo}proveedor (
    PRV_DESCRIPCION, PRV_CELULAR1, PRV_CELULAR2, PRV_DIRECCION, PRV_OBSERVACION, PRV_VIGENTE
) VALUES (%s, %s, %s, %s, %s, %s)
""", proveedores)

# ==== OBTENER IDS NECESARIOS ====

cursor.execute(f"SELECT PER_ID FROM {modulo}persona")
persona_ids = [row[0] for row in cursor.fetchall()]

cursor.execute(f"SELECT USU_ID FROM {modulo}usuario")
usuario_ids = [row[0] for row in cursor.fetchall()]

cursor.execute(f"SELECT COC_ID FROM {modulo}concepto_contable")
concepto_ids = [row[0] for row in cursor.fetchall()]

cursor.execute(f"SELECT CUR_ID FROM {modulo}curso")
curso_ids = [row[0] for row in cursor.fetchall()]

# ==== PAGO_PERSONA ====

pagos_persona = []
for _ in range(20):
    per_id = random.choice(persona_ids)
    cur_id = random.choice(curso_ids)
    usu_id = random.choice(usuario_ids)
    pagos_persona.append((
        per_id,
        cur_id,
        usu_id,
        datetime.now() - timedelta(days=random.randint(0, 30)),
        round(random.uniform(10000, 500000), 2),  # valor
        fake.sentence(nb_words=10)[:500]
    ))

insert_many(f"""
INSERT INTO {modulo}pago_persona (
    PER_ID, CUR_ID, USU_ID, PAP_FECHA_HORA, PAP_VALOR, PAP_OBSERVACION
) VALUES (%s, %s, %s, %s, %s, %s)
""", pagos_persona)

cursor.execute(f"SELECT PAP_ID FROM {modulo}pago_persona")
pago_persona_ids = [row[0] for row in cursor.fetchall()]

# ==== COMPROBANTE_PAGO ====

comprobantes = []
for _ in range(15):
    usu_id = random.choice(usuario_ids)
    pec_id = random.choice(curso_ids)  # aquí normalmente sería un PEC_ID real relacionado a PersonaCurso
    coc_id = random.choice(concepto_ids)
    fecha_hora = datetime.now() - timedelta(days=random.randint(0, 30))
    fecha = fecha_hora.date()
    numero = random.randint(1000, 9999)
    valor = round(random.uniform(5000, 300000), 2)
    comprobantes.append((usu_id, pec_id, coc_id, fecha_hora, fecha, numero, valor))

insert_many(f"""
INSERT INTO {modulo}comprobante_pago (
    USU_ID, PEC_ID, COC_ID, CPA_FECHA_HORA, CPA_FECHA, CPA_NUMERO, CPA_VALOR
) VALUES (%s, %s, %s, %s, %s, %s, %s)
""", comprobantes)

cursor.execute(f"SELECT CPA_ID FROM {modulo}comprobante_pago")
comprobante_ids = [row[0] for row in cursor.fetchall()]

# ==== PAGO_COMPROBANTE ====

pago_comprobantes = []
for _ in range(10):
    pap_id = random.choice(pago_persona_ids)
    cpa_id = random.choice(comprobante_ids)
    pago_comprobantes.append((pap_id, cpa_id))

insert_many(f"""
INSERT INTO {modulo}pago_comprobante (
    PAP_ID, CPA_ID
) VALUES (%s, %s)
""", pago_comprobantes)

# ==== PREPAGO ====

prepagos = []
for _ in range(15):
    per_id = random.choice(persona_ids)
    cur_id = random.choice(curso_ids)
    pap_id = random.choice(pago_persona_ids + [None])  # Puede ser NULL
    valor = round(random.uniform(5000, 200000), 2)
    observacion = fake.sentence(nb_words=10)[:500]
    vigente = random.choice([True, True, True, False])
    prepagos.append((per_id, cur_id, pap_id, valor, observacion, vigente))

insert_many(f"""
INSERT INTO {modulo}prepago (
    PER_ID, CUR_ID, PAP_ID, PPA_VALOR, PPA_OBSERVACION, PPA_VIGENTE
) VALUES (%s, %s, %s, %s, %s, %s)
""", prepagos)

print("✅ Datos de Proveedor, Pago_Persona, Comprobante y Prepago insertados correctamente")
cursor.close()
db.close()
