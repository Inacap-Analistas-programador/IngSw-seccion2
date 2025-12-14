
import sys

filepath = r"d:\IngSw-seccion2\SystemScoutsClient\src\views\Gestionpersonas.vue"

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if "abrirModalPersona" in line:
            print(f"Match 'abrirModalPersona' at line {i+1}: {line.strip()}")

except Exception as e:
    print(f"Error reading file: {e}")
