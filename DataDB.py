import sys
import subprocess

# Lista de scripts a ejecutar en orden
scripts = [
    "DataDB_Usuario.py",
    "DataDB_Mantenedor.py",
    "DataDB_Persona.py",
    "DataDB_Curso.py",
    "DataDB_Archivo.py",
    "DataDB_Pago.py",
]

for s in scripts:
    print(f"Ejecutando {s}...")
    result = subprocess.run([sys.executable, s], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error en {s}:")
        print(result.stderr)
        break
