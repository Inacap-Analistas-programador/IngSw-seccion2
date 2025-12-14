
import sys

filepath = r"d:\IngSw-seccion2\SystemScoutsClient\src\views\Gestionpersonas.vue"

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        # Check for the pattern in the error message
        if "} catch {" in line:
            print(f"Match '}} catch {{' at line {i+1}: {line.strip()}")
            # Print context
            start = max(0, i-2)
            end = min(len(lines), i+3)
            for j in range(start, end):
                print(f"{j+1}: {lines[j].strip()}")
                
        # Check for empty string check in error message
        if "/* ignore */" in line:
            print(f"Match '/* ignore */' at line {i+1}: {line.strip()}")

        if "Si el backend falla" in line:
             print(f"Match 'Si el backend falla' at line {i+1}: {line.strip()}")

except Exception as e:
    print(f"Error reading file: {e}")
