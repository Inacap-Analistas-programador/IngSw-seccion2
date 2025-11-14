import sys
import subprocess
import os
from datetime import datetime

# ============================================
# 🧩 Configuración
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "")

scripts = [
    "DataDB_Mantenedor.py",
    "DataDB_Persona.py",
    "DataDB_Curso.py",
    "DataDB_Archivo.py",
    "DataDB_Pago.py",
]

# ============================================
# 🎨 Funciones auxiliares
# ============================================
def print_header(title):
    print("\n" + "=" * 60)
    print(f"🔹 {title}")
    print("=" * 60 + "\n")

# ============================================
# 🚀 Ejecución
# ============================================
print_header("INICIO DE POBLADO DE BASE DE DATOS")

for script in scripts:
    script_path = os.path.join(DATA_PATH, script)
    print(f"▶ Ejecutando {script_path} ...\n")

    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {script} completado correctamente.\n")
    else:
        print("🛑 Ejecución detenida por error.")
        break

print_header("FIN DEL POBLADO")
