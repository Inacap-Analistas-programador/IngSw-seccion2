import os
import sys
import django
import pymysql

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from django.conf import settings

# Database connection
db_config = settings.DATABASES['default']
connection = pymysql.connect(
    host=db_config['HOST'],
    user=db_config['USER'],
    password=db_config['PASSWORD'],
    database=db_config['NAME'],
    port=int(db_config['PORT'])
)

cursor = connection.cursor()

print("=" * 60)
print("CORRIGIENDO ESQUEMA DE BASE DE DATOS")
print("=" * 60)
print()

def column_exists(table_name, column_name):
    """Check if column exists in table"""
    cursor.execute("""
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = %s
        AND COLUMN_NAME = %s
    """, (table_name, column_name))
    return cursor.fetchone()[0] > 0

# Fix PERSONA table
print("📝 Verificando tabla PERSONA...")
if not column_exists('persona', 'per_apelpat'):
    print("   ⚠️  Columna per_apelpat no existe. Agregando...")
    cursor.execute("""
        ALTER TABLE persona 
        ADD COLUMN per_apelpat VARCHAR(50) NOT NULL DEFAULT ''
    """)
    print("   ✅ Columna per_apelpat agregada")
else:
    print("   ✓ Columna per_apelpat existe")

if not column_exists('persona', 'per_email'):
    print("   ⚠️  Columna per_email no existe. Agregando...")
    cursor.execute("""
        ALTER TABLE persona 
        ADD COLUMN per_email VARCHAR(100) NOT NULL DEFAULT ''
    """)
    print("   ✅ Columna per_email agregada")
else:
    print("   ✓ Columna per_email existe")

if not column_exists('persona', 'per_num_mmaa'):
    print("   ⚠️  Columna per_num_mmaa no existe. Agregando...")
    cursor.execute("""
        ALTER TABLE persona 
        ADD COLUMN per_num_mmaa INT NULL
    """)
    print("   ✅ Columna per_num_mmaa agregada")
else:
    print("   ✓ Columna per_num_mmaa existe")

# Fix CURSO table
print()
print("📝 Verificando tabla CURSO...")
if not column_exists('curso', 'cur_cuota_con_almuerzo'):
    print("   ⚠️  Columna cur_cuota_con_almuerzo no existe. Agregando...")
    cursor.execute("""
        ALTER TABLE curso 
        ADD COLUMN cur_cuota_con_almuerzo INT NOT NULL DEFAULT 0
    """)
    print("   ✅ Columna cur_cuota_con_almuerzo agregada")
else:
    print("   ✓ Columna cur_cuota_con_almuerzo existe")

if not column_exists('curso', 'cur_cuota_sin_almuerzo'):
    print("   ⚠️  Columna cur_cuota_sin_almuerzo no existe. Agregando...")
    cursor.execute("""
        ALTER TABLE curso 
        ADD COLUMN cur_cuota_sin_almuerzo INT NOT NULL DEFAULT 0
    """)
    print("   ✅ Columna cur_cuota_sin_almuerzo agregada")
else:
    print("   ✓ Columna cur_cuota_sin_almuerzo existe")

# Fix CURSO_CUOTA table - check if cuu_fecha is DATE instead of DATETIME
print()
print("📝 Verificando tabla CURSO_CUOTA...")
cursor.execute("""
    SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'curso_cuota'
    AND COLUMN_NAME = 'cuu_fecha'
""")
result = cursor.fetchone()
if result and result[0] == 'date':
    print("   ⚠️  Columna cuu_fecha es DATE, debe ser DATETIME. Modificando...")
    cursor.execute("""
        ALTER TABLE curso_cuota 
        MODIFY COLUMN cuu_fecha DATETIME NOT NULL
    """)
    print("   ✅ Columna cuu_fecha modificada a DATETIME")
else:
    print("   ✓ Columna cuu_fecha es DATETIME")

# Fix CURSO table - check DATE fields that should be DATETIME
print()
print("📝 Verificando columnas de fechas en tabla CURSO...")

# Check cur_fecha_solicitud
cursor.execute("""
    SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'curso'
    AND COLUMN_NAME = 'cur_fecha_solicitud'
""")
result = cursor.fetchone()
if result and result[0] == 'date':
    print("   ⚠️  Columna cur_fecha_solicitud es DATE, debe ser DATETIME. Modificando...")
    cursor.execute("""
        ALTER TABLE curso 
        MODIFY COLUMN cur_fecha_solicitud DATETIME NOT NULL
    """)
    print("   ✅ Columna cur_fecha_solicitud modificada a DATETIME")
else:
    print("   ✓ Columna cur_fecha_solicitud es DATETIME")

# Fix CURSO_FECHA table
print()
print("📝 Verificando columnas de fechas en tabla CURSO_FECHA...")

cursor.execute("""
    SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'curso_fecha'
    AND COLUMN_NAME = 'cuf_fecha_inicio'
""")
result = cursor.fetchone()
if result and result[0] == 'date':
    print("   ⚠️  Columna cuf_fecha_inicio es DATE, debe ser DATETIME. Modificando...")
    cursor.execute("""
        ALTER TABLE curso_fecha 
        MODIFY COLUMN cuf_fecha_inicio DATETIME NOT NULL
    """)
    print("   ✅ Columna cuf_fecha_inicio modificada a DATETIME")
else:
    print("   ✓ Columna cuf_fecha_inicio es DATETIME")

cursor.execute("""
    SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'curso_fecha'
    AND COLUMN_NAME = 'cuf_fecha_termino'
""")
result = cursor.fetchone()
if result and result[0] == 'date':
    print("   ⚠️  Columna cuf_fecha_termino es DATE, debe ser DATETIME. Modificando...")
    cursor.execute("""
        ALTER TABLE curso_fecha 
        MODIFY COLUMN cuf_fecha_termino DATETIME NOT NULL
    """)
    print("   ✅ Columna cuf_fecha_termino modificada a DATETIME")
else:
    print("   ✓ Columna cuf_fecha_termino es DATETIME")

# Commit changes
connection.commit()

print()
print("=" * 60)
print("✅ ESQUEMA DE BASE DE DATOS CORREGIDO EXITOSAMENTE")
print("=" * 60)

cursor.close()
connection.close()
