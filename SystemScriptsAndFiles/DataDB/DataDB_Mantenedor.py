import mysql.connector
from faker import Faker
import random
import os

fake = Faker('es_CL')

# 🔧 Conexión a la base de datos
conexion = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD_DB"),
    database=os.getenv("DATABASE")
)
cursor = conexion.cursor()

def poblar_tablas_basicas():
    # --- ROL ---
    roles = [
        ('Participante', 1),
        ('Formadores', 2),
        ('Apoyo Formadores', 3),
        ('Organización', 4),
        ('Servicio', 5),
        ('Salud', 6)
    ]
    for desc, tipo in roles:
        cursor.execute("""
            INSERT INTO ROL (ROL_DESCRIPCION, ROL_TIPO, ROL_VIGENTE)
            VALUES (%s, %s, %s)
        """, (desc, tipo, True))

    # --- CARGO ---
    cargos = [
        'Jefe de Grupo', 'Subjefe de Grupo', 'Tesorero', 'Secretario',
        'Encargado de Comunicaciones', 'Instructor de Rama', 'Apoyo Logístico'
    ]
    for c in cargos:
        cursor.execute("INSERT INTO CARGO (CAR_DESCRIPCION, CAR_VIGENTE) VALUES (%s, %s)", (c, True))

    # --- RAMA ---
    ramas = ['Manada', 'Tropa', 'Comunidad', 'Clan', 'Dirigentes']
    for r in ramas:
        cursor.execute("INSERT INTO RAMA (RAM_DESCRIPCION, RAM_VIGENTE) VALUES (%s, %s)", (r, True))

    # --- ESTADO CIVIL ---
    estados_civiles = ['Soltero', 'Casado', 'Divorciado', 'Viudo', 'Unión Civil']
    for e in estados_civiles:
        cursor.execute("INSERT INTO ESTADO_CIVIL (ESC_DESCRIPCION, ESC_VIGENTE) VALUES (%s, %s)", (e, True))

    # --- NIVEL ---
    niveles = [
        ('Nivel 1 - Básico', 1),
        ('Nivel 2 - Medio', 2),
        ('Nivel 3 - Avanzado', 3),
        ('Nivel 4 - Especialista', 4)
    ]
    for desc, orden in niveles:
        cursor.execute("INSERT INTO NIVEL (NIV_DESCRIPCION, NIV_ORDEN, NIV_VIGENTE) VALUES (%s, %s, %s)", (desc, orden, True))

    # --- ZONA ---
    zonas = ['Zona Norte', 'Zona Centro', 'Zona Sur', 'Zona Austral']
    for z in zonas:
        cursor.execute("""
            INSERT INTO ZONA (ZON_DESCRIPCION, ZON_UNILATERAL, ZON_VIGENTE)
            VALUES (%s, %s, %s)
        """, (z, False, True))

    # --- REGION ---
    regiones = ['Región Metropolitana', 'Valparaíso', 'Biobío', 'Araucanía', 'Los Lagos']
    for r in regiones:
        cursor.execute("INSERT INTO REGION (REG_DESCRIPCION, REG_VIGENTE) VALUES (%s, %s)", (r, True))

    conexion.commit()

def poblar_dependientes():
    # Obtener IDs base
    cursor.execute("SELECT ZON_ID FROM ZONA")
    zonas = [z[0] for z in cursor.fetchall()]

    cursor.execute("SELECT REG_ID FROM REGION")
    regiones = [r[0] for r in cursor.fetchall()]

    # --- DISTRITO ---
    for i in range(1, 9):
        cursor.execute("""
            INSERT INTO DISTRITO (ZON_ID, DIS_DESCRIPCION, DIS_VIGENTE)
            VALUES (%s, %s, %s)
        """, (random.choice(zonas), f"Distrito {i}", True))

    # --- PROVINCIA ---
    for i in range(1, 9):
        cursor.execute("""
            INSERT INTO PROVINCIA (REG_ID, PRO_DESCRIPCION, PRO_VIGENTE)
            VALUES (%s, %s, %s)
        """, (random.choice(regiones), f"Provincia {i}", True))

    conexion.commit()

    # Obtener IDs actualizados
    cursor.execute("SELECT DIS_ID FROM DISTRITO")
    distritos = [d[0] for d in cursor.fetchall()]

    cursor.execute("SELECT PRO_ID FROM PROVINCIA")
    provincias = [p[0] for p in cursor.fetchall()]

    # --- GRUPO ---
    for i in range(1, 11):
        cursor.execute("""
            INSERT INTO GRUPO (DIS_ID, GRU_DESCRIPCION, GRU_VIGENTE)
            VALUES (%s, %s, %s)
        """, (random.choice(distritos), f"Grupo {i}", True))

    # --- COMUNA ---
    for i in range(1, 11):
        cursor.execute("""
            INSERT INTO COMUNA (PRO_ID, COM_DESCRIPCION, COM_VIGENTE)
            VALUES (%s, %s, %s)
        """, (random.choice(provincias), f"Comuna {i}", True))

    conexion.commit()

def poblar_restantes():
    # --- ALIMENTACION ---
    alimentaciones = [
        ('Almuerzo Completo', 1),
        ('Sin Almuerzo', 2),
        ('Vegetariano', 1),
        ('Vegano', 1),
    ]
    for desc, tipo in alimentaciones:
        cursor.execute("""
            INSERT INTO ALIMENTACION (ALI_DESCRIPCION, ALI_TIPO, ALI_VIGENTE)
            VALUES (%s, %s, %s)
        """, (desc, tipo, True))

    # --- CONCEPTO CONTABLE ---
    conceptos = ['Inscripción', 'Aporte de Zona', 'Aporte de Grupo', 'Donación', 'Mantenimiento']
    for c in conceptos:
        cursor.execute("""
            INSERT INTO CONCEPTO_CONTABLE (COC_DESCRIPCION, COC_VIGENTE)
            VALUES (%s, %s)
        """, (c, True))

    # --- TIPO CURSO ---
    tipos_curso = [
        ('Curso Inicial de Formación', 1, 30),
        ('Curso Medio de Liderazgo', 2, 25),
        ('Curso Avanzado de Dirigencia', 3, 20),
        ('Habilitación Especial', 4, 15),
        ('Verificación Técnica', 5, 10)
    ]
    for desc, tipo, cant in tipos_curso:
        cursor.execute("""
            INSERT INTO TIPO_CURSO (TCU_DESCRIPCION, TCU_TIPO, TCU_CANT_PARTICIPANTE, TCU_VIGENTE)
            VALUES (%s, %s, %s, %s)
        """, (desc, tipo, cant, True))

    # --- TIPO ARCHIVO ---
    archivos = ['PDF', 'Imagen', 'Video', 'Documento Word', 'Excel']
    for a in archivos:
        cursor.execute("""
            INSERT INTO TIPO_ARCHIVO (TAR_DESCRIPCION, TAR_VIGENTE)
            VALUES (%s, %s)
        """, (a, True))

    conexion.commit()

# 🚀 Ejecución
if __name__ == "__main__":
    poblar_tablas_basicas()
    poblar_dependientes()
    poblar_restantes()
    print("✅ Poblamiento completado correctamente.")
