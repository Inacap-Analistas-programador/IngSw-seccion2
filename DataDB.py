import subprocess

# Lista de scripts a ejecutar en orden
scripts = [
    "DataDB_Archivo.py",
    "DataDB_Curso.py",
    "DataDB_Mantenedor.py",
    "DataDB_Pago.py",
    "DataDB_Usuario.py",
]

for s in scripts:
    print(f"Ejecutando {s}...")
    result = subprocess.run(["python", s], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error en {s}:")
        print(result.stderr)
        break  # detener ejecución si hay error
