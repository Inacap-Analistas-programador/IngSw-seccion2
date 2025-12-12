import re

try:
    with open('error_log.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all occurrences of file paths in the project
    matches = re.findall(r'(d:.*?SystemScoutsApi.*?\.py)', content, re.IGNORECASE)
    
    print("Files found in traceback:")
    for m in set(matches):
        print(f" - {m}")
        
    # Try to find the specific error location with context
    # Usually Django debug page puts the file path in <code> or similar
    # Simple search for lines with the path
    print("\nLines with project path:")
    blocks = re.split(r'<li class="frame">', content)
    for block in blocks:
        if 'SystemScoutsApi' in block:
            # Extract filename and line number
            match = re.search(r'(d:[^<]*?SystemScoutsApi[^<]*?\.py)"', block, re.IGNORECASE)
            if match:
                path = match.group(1)
                # Find line number (often in <span class="lineno">)
                lineno_match = re.search(r'<span class="lineno">(\d+)</span>', block)
                lineno = lineno_match.group(1) if lineno_match else "?"
                print(f"File: {path}, Line: {lineno}")
                
except Exception as e:
    print(f"Error parsing: {e}")
