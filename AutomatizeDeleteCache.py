import os
import shutil

# Ruta raíz desde donde quieres limpiar
root_dir = r"D:\SistemaScoutsCursoMedio\IngSw-seccion2\SystemScoutsApi"  # Cambia esto a tu proyecto

for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
    # Eliminar __pycache__ si existe
    if "__pycache__" in dirnames:
        cache_path = os.path.join(dirpath, "__pycache__")
        shutil.rmtree(cache_path)
        print(f"Eliminada carpeta: {cache_path}")
    
    # Eliminar carpetas migrations, excepto __init__.py si quieres conservarlo
    if "migrations" in dirnames:
        mig_path = os.path.join(dirpath, "migrations")
        # Opcional: conservar __init__.py
        for file in os.listdir(mig_path):
            if file != "__init__.py":
                file_path = os.path.join(mig_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path)
        shutil.rmtree(mig_path)
        print(f"Limpieza realizada en carpeta: {mig_path}")
