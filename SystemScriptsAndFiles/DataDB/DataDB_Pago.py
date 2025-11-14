import mysql.connector
from faker import Faker
import random
import os
from datetime import datetime, timedelta
from decimal import Decimal

fake = Faker('es_CL')

# 🔧 Conexión a la base de datos
conexion = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD_DB"),
    database=os.getenv("DATABASE")
)
cursor = conexion.cursor()

# ------------------------------------------------------------
# 🧩 FUNCIONES DE APOYO
# ------------------------------------------------------------
def obtener_ids(tabla, campo):
    cursor.execute(f"SELECT {campo} FROM {tabla}")
    return [r[0] for r in cursor.fetchall()]

# ------------------------------------------------------------
# 🧱 1. POBLAR PROVEEDORES
# ------------------------------------------------------------
def poblar_proveedores(cantidad=10):
    for _ in range(cantidad):
        desc = fake.company()
        cel1 = f"+56 9 {random.randint(40000000, 99999999)}"
        cel2 = f"+56 9 {random.randint(40000000, 99999999)}" if random.choice([True, False]) else None
        direccion = fake.address().replace('\n', ' ')
        obs = fake.sentence(nb_words=10)
        cursor.execute("""
            INSERT INTO PROVEEDOR (
                PRV_DESCRIPCION, PRV_CELULAR1, PRV_CELULAR2,
                PRV_DIRECCION, PRV_OBSERVACION, PRV_VIGENTE
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (desc, cel1, cel2, direccion, obs, True))
    conexion.commit()
    print(f"✅ Se poblaron {cantidad} proveedores.")

# ------------------------------------------------------------
# 💰 2. POBLAR COMPROBANTES DE PAGO
# ------------------------------------------------------------
def poblar_comprobantes(cantidad=20):
    usuarios = obtener_ids("USUARIO", "USU_ID")
    cursos = obtener_ids("CURSO", "CUR_ID")
    conceptos = obtener_ids("CONCEPTO_CONTABLE", "COC_ID")

    if not usuarios or not cursos or not conceptos:
        print("⚠️ Faltan datos base en USUARIO, CURSO o CONCEPTO_CONTABLE.")
        return

    for i in range(cantidad):
        usu = random.choice(usuarios)
        cur = random.choice(cursos)
        coc = random.choice(conceptos)
        fecha_hora = fake.date_time_between(start_date="-90d", end_date="now")
        numero = random.randint(1000, 9999)
        valor = round(random.uniform(5000, 80000), 2)

        cursor.execute("""
            INSERT INTO COMPROBANTE_PAGO (
                USU_ID, PEC_ID, COC_ID,
                CPA_FECHA_HORA, CPA_FECHA, CPA_NUMERO, CPA_VALOR
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (usu, cur, coc, fecha_hora, fecha_hora.date(), numero, valor))
    conexion.commit()
    print(f"✅ Se poblaron {cantidad} comprobantes de pago.")

# ------------------------------------------------------------
# 🧾 3. POBLAR PAGOS DE PERSONAS
# ------------------------------------------------------------
def poblar_pagos_personas(cantidad=30):
    personas = obtener_ids("PERSONA", "PER_ID")
    cursos = obtener_ids("CURSO", "CUR_ID")
    usuarios = obtener_ids("USUARIO", "USU_ID")

    if not personas or not cursos or not usuarios:
        print("⚠️ Faltan datos base en PERSONA, CURSO o USUARIO.")
        return

    for _ in range(cantidad):
        per = random.choice(personas)
        cur = random.choice(cursos)
        usu = random.choice(usuarios)
        fecha_hora = fake.date_time_between(start_date="-60d", end_date="now")
        tipo = random.choice([1, 2])  # Ingreso o Egreso
        estado = random.choice([1, 2])  # Pagado o Anulado
        valor = Decimal(round(random.uniform(10000, 150000), 2))
        observacion = fake.sentence(nb_words=6)

        cursor.execute("""
            INSERT INTO PAGO_PERSONA (
                PER_ID, CUR_ID, USU_ID, PAP_FECHA_HORA,
                PAP_TIPO, PAP_VALOR, PAP_ESTADO, PAP_OBSERVACION
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (per, cur, usu, fecha_hora, tipo, valor, estado, observacion))

    conexion.commit()
    print(f"✅ Se poblaron {cantidad} pagos de personas.")

# ------------------------------------------------------------
# 🧮 4. POBLAR PAGO_COMPROBANTE
# ------------------------------------------------------------
def poblar_pago_comprobante(cantidad=15):
    cursor.execute("SELECT PAP_ID FROM PAGO_PERSONA")
    pagos = [p[0] for p in cursor.fetchall()]
    cursor.execute("SELECT CPA_ID FROM COMPROBANTE_PAGO")
    comprobantes = [c[0] for c in cursor.fetchall()]

    if not pagos or not comprobantes:
        print("⚠️ Faltan registros en PAGO_PERSONA o COMPROBANTE_PAGO.")
        return

    for _ in range(cantidad):
        pap = random.choice(pagos)
        cpa = random.choice(comprobantes)
        cursor.execute("""
            INSERT INTO PAGO_COMPROBANTE (PAP_ID, CPA_ID)
            VALUES (%s, %s)
        """, (pap, cpa))

    conexion.commit()
    print(f"✅ Se poblaron {cantidad} asociaciones PAGO_COMPROBANTE.")

# ------------------------------------------------------------
# 💳 5. POBLAR PREPAGO
# ------------------------------------------------------------
def poblar_prepago(cantidad=10):
    personas = obtener_ids("PERSONA", "PER_ID")
    cursos = obtener_ids("CURSO", "CUR_ID")
    cursor.execute("SELECT PAP_ID FROM PAGO_PERSONA")
    pagos = [p[0] for p in cursor.fetchall()]

    if not personas or not cursos:
        print("⚠️ Faltan PERSONAS o CURSOS para crear PREPAGOS.")
        return

    for _ in range(cantidad):
        per = random.choice(personas)
        cur = random.choice(cursos)
        pap = random.choice(pagos) if pagos else None
        valor = Decimal(round(random.uniform(5000, 50000), 2))
        observacion = fake.sentence(nb_words=8)

        cursor.execute("""
            INSERT INTO PREPAGO (PER_ID, CUR_ID, PAP_ID, PPA_VALOR, PPA_OBSERVACION, PPA_VIGENTE)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (per, cur, pap, valor, observacion, True))

    conexion.commit()
    print(f"✅ Se poblaron {cantidad} prepagos.")

# ------------------------------------------------------------
# 🚀 EJECUCIÓN PRINCIPAL
# ------------------------------------------------------------
if __name__ == "__main__":
    poblar_proveedores()
    poblar_comprobantes()
    poblar_pagos_personas()
    poblar_pago_comprobante()
    poblar_prepago()
    print("\n🎉 Poblamiento de módulo de pagos completado correctamente.")
