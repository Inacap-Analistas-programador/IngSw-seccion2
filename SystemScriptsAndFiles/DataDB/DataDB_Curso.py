import mysql.connector
from faker import Faker
import random
import os
from datetime import timedelta

# ============================
# CONFIGURACIÓN DE CONEXIÓN
# ============================
connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD_DB"),
    database=os.getenv("DATABASE")
)
cursor = connection.cursor()
fake = Faker('es_CL')

# ============================
# FUNCIONES AUXILIARES
# ============================

def get_random_id(table, column):
    cursor.execute(f"SELECT {column} FROM {table} ORDER BY RAND() LIMIT 1;")
    result = cursor.fetchone()
    return result[0] if result else None

def generar_codigo_unico():
    """Genera un CUR_CODIGO único que no exista en la tabla CURSO."""
    while True:
        codigo = f"CUR-{random.randint(1000, 9999)}"
        cursor.execute("SELECT COUNT(*) FROM CURSO WHERE CUR_CODIGO = %s", (codigo,))
        if cursor.fetchone()[0] == 0:
            return codigo


# ============================
# POBLAR CURSO
# ============================

def poblar_curso(n=10):
    print(f"Insertando {n} cursos...")
    for _ in range(n):
        USU_ID = get_random_id("USUARIO", "USU_ID")
        TCU_ID = get_random_id("TIPO_CURSO", "TCU_ID")
        PER_ID_RESPONSABLE = get_random_id("PERSONA", "PER_ID")
        CAR_ID_RESPONSABLE = get_random_id("CARGO", "CAR_ID")
        COM_ID_LUGAR = get_random_id("COMUNA", "COM_ID")

        fecha_hora = fake.date_time_between(start_date='-1y', end_date='now')
        fecha_solicitud = fecha_hora.date()
        codigo = generar_codigo_unico()  # ✅ Garantiza unicidad
        descripcion = fake.sentence(nb_words=6)
        observacion = fake.text(max_nb_chars=80) if random.choice([True, False]) else None
        administra = random.randint(1, 2)
        cota_con = random.randint(10000, 50000)
        cota_sin = random.randint(5000, 30000)
        modalidad = random.randint(1, 3)
        tipo_curso = random.randint(1, 3)
        lugar = fake.city()
        latitud = str(round(random.uniform(-56.0, -17.0), 6))
        longitud = str(round(random.uniform(-75.0, -66.0), 6))
        estado = random.randint(0, 3)

        cursor.execute("""
            INSERT INTO CURSO (
                USU_ID, TCU_ID, PER_ID_RESPONSABLE, CAR_ID_RESPONSABLE, COM_ID_LUGAR,
                CUR_FECHA_HORA, CUR_FECHA_SOLICITUD, CUR_CODIGO, CUR_DESCRIPCION, CUR_OBSERVACION,
                CUR_ADMINISTRA, CUR_COTA_CON_ALMUERZO, CUR_COTA_SIN_ALMUERZO,
                CUR_MODALIDAD, CUR_TIPO_CURSO, CUR_LUGAR, CUR_COORD_LATITUD,
                CUR_COORD_LONGITUD, CUR_ESTADO
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            USU_ID, TCU_ID, PER_ID_RESPONSABLE, CAR_ID_RESPONSABLE, COM_ID_LUGAR,
            fecha_hora, fecha_solicitud, codigo, descripcion, observacion, administra,
            cota_con, cota_sin, modalidad, tipo_curso, lugar, latitud, longitud, estado
        ))
        connection.commit()


# ============================
# POBLAR CURSO_CUOTA
# ============================

def poblar_curso_cuota():
    cursor.execute("SELECT CUR_ID, CUR_FECHA_SOLICITUD FROM CURSO;")
    cursos = cursor.fetchall()
    for CUR_ID, fecha_solicitud in cursos:
        for tipo in [1, 2]:
            valor = random.uniform(10000, 50000)
            cursor.execute("""
                INSERT INTO CURSO_CUOTA (CUR_ID, CUU_TIPO, CUU_FECHA, CUU_VALOR)
                VALUES (%s, %s, %s, %s)
            """, (CUR_ID, tipo, fecha_solicitud, valor))
    connection.commit()

# ============================
# POBLAR CURSO_FECHA
# ============================

def poblar_curso_fecha():
    cursor.execute("SELECT CUR_ID, CUR_FECHA_SOLICITUD FROM CURSO;")
    cursos = cursor.fetchall()
    for CUR_ID, fecha_solicitud in cursos:
        fecha_inicio = fecha_solicitud + timedelta(days=random.randint(5, 20))
        fecha_termino = fecha_inicio + timedelta(days=random.randint(3, 10))
        tipo = random.randint(1, 3)
        cursor.execute("""
            INSERT INTO CURSO_FECHA (CUR_ID, CUF_FECHA_INICIO, CUF_FECHA_TERMINO, CUF_TIPO)
            VALUES (%s, %s, %s, %s)
        """, (CUR_ID, fecha_inicio, fecha_termino, tipo))
    connection.commit()

# ============================
# POBLAR CURSO_ALIMENTACION
# ============================

def poblar_curso_alimentacion():
    cursor.execute("SELECT CUR_ID, CUR_FECHA_SOLICITUD FROM CURSO;")
    cursos = cursor.fetchall()
    for CUR_ID, fecha_solicitud in cursos:
        ALI_ID = get_random_id("ALIMENTACION", "ALI_ID")
        fecha = fecha_solicitud + timedelta(days=random.randint(1, 5))
        tiempo = random.randint(1, 5)
        descripcion = f"{fake.word()} especial"
        cantidad = random.randint(0, 20)
        vigente = random.choice([True, False])
        cursor.execute("""
            INSERT INTO CURSO_ALIMENTACION
            (CUR_ID, ALI_ID, CUA_FECHA, CUA_TIEMPO, CUA_DESCRIPCION, CUA_CANTIDAD_ADICIONAL, CUA_VIGENTE)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (CUR_ID, ALI_ID, fecha, tiempo, descripcion, cantidad, vigente))
    connection.commit()

# ============================
# POBLAR CURSO_COORDINADOR
# ============================

def poblar_curso_coordinador():
    cursor.execute("SELECT CUR_ID FROM CURSO;")
    cursos = cursor.fetchall()
    for CUR_ID, in cursos:
        PER_ID = get_random_id("PERSONA", "PER_ID")
        CAR_ID = get_random_id("CARGO", "CAR_ID")
        cargo = fake.job()
        cursor.execute("""
            INSERT INTO CURSO_COORDINADOR (CUR_ID, PER_ID, CAR_ID, CUC_CARGO)
            VALUES (%s,%s,%s,%s)
        """, (CUR_ID, PER_ID, CAR_ID, cargo))
    connection.commit()

# ============================
# POBLAR CURSO_SECCION
# ============================

def poblar_curso_seccion():
    cursor.execute("SELECT CUR_ID FROM CURSO;")
    cursos = cursor.fetchall()
    for CUR_ID, in cursos:
        RAM_ID = get_random_id("RAMA", "RAM_ID")
        seccion = random.randint(1, 10)
        cantidad = random.randint(10, 50)
        cursor.execute("""
            INSERT INTO CURSO_SECCION (CUR_ID, RAM_ID, CUS_SECCION, CUS_CANT_PARTICIPANTE)
            VALUES (%s,%s,%s,%s)
        """, (CUR_ID, RAM_ID, seccion, cantidad))
    connection.commit()

# ============================
# POBLAR CURSO_FORMADOR
# ============================

def poblar_curso_formador():
    cursor.execute("SELECT CUS_ID, CUR_ID FROM CURSO_SECCION;")
    secciones = cursor.fetchall()
    for CUS_ID, CUR_ID in secciones:
        PER_ID = get_random_id("PERSONA", "PER_ID")
        ROL_ID = get_random_id("ROL", "ROL_ID")
        director = random.choice([True, False])
        cursor.execute("""
            INSERT INTO CURSO_FORMADOR (CUR_ID, PER_ID, ROL_ID, CUS_ID, CUO_DIRECTOR)
            VALUES (%s,%s,%s,%s,%s)
        """, (CUR_ID, PER_ID, ROL_ID, CUS_ID, director))
    connection.commit()

# ============================
# EJECUCIÓN
# ============================

if __name__ == "__main__":
    poblar_curso(100)
    poblar_curso_cuota()
    poblar_curso_fecha()
    poblar_curso_alimentacion()
    poblar_curso_coordinador()
    poblar_curso_seccion()
    poblar_curso_formador()
    print("✅ Poblamiento completo de CURSO y sus tablas asociadas.")

    cursor.close()
    connection.close()