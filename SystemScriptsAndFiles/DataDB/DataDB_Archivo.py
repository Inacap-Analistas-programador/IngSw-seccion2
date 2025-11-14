import mysql.connector
from faker import Faker
import random
import os
from datetime import datetime

# ============================================
# 🔧 CONFIGURACIÓN DE CONEXIÓN
# ============================================
conexion = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD_DB"),
    database=os.getenv("DATABASE")
)
cursor = conexion.cursor()
fake = Faker('es_CL')

# ============================================
# 🔍 FUNCIONES AUXILIARES
# ============================================
def obtener_ids(tabla, campo):
    cursor.execute(f"SELECT {campo} FROM {tabla}")
    return [fila[0] for fila in cursor.fetchall()]

# ============================================
# 📦 FUNCIÓN PRINCIPAL
# ============================================
def poblar_archivo(num_archivos=10):
    try:
        TAR_IDs = obtener_ids('TIPO_ARCHIVO', 'TAR_ID')
        USU_IDs = obtener_ids('USUARIO', 'USU_ID')

        if not TAR_IDs or not USU_IDs:
            print("❌ No hay datos suficientes en TIPO_ARCHIVO o USUARIO.")
            return

        data = []
        for _ in range(num_archivos):
            TAR_ID = random.choice(TAR_IDs)
            USU_CREA = random.choice(USU_IDs)
            USU_MODIFICA = random.choice(USU_IDs)

            ARC_DESCRIPCION = fake.sentence(nb_words=6)
            ARC_RUTA = f"/archivos/{fake.file_name(extension='pdf')}"
            ARC_VIGENTE = random.choice([True, False])

            data.append((
                TAR_ID,
                USU_CREA,
                USU_MODIFICA,
                ARC_DESCRIPCION,
                ARC_RUTA,
                ARC_VIGENTE
            ))

        query = """
            INSERT INTO ARCHIVO (
                TAR_ID,
                USU_ID_CREA,
                USU_ID_MODIFICA,
                ARC_DESCRIPCION,
                ARC_RUTA,
                ARC_VIGENTE,
                ARC_FECHA_HORA
            ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """

        cursor.executemany(query, data)
        conexion.commit()
        print(f"✅ Se insertaron {cursor.rowcount} registros en ARCHIVO.")

    except mysql.connector.Error as err:
        print(f"❌ Error MySQL: {err}")
        conexion.rollback()
    except Exception as e:
        print(f"⚠️ Error general: {e}")
        conexion.rollback()

# ============================================
# 🚀 EJECUCIÓN
# ============================================
if __name__ == "__main__":
    poblar_archivo(100)  # Puedes cambiar el número
    cursor.close()
    conexion.close()