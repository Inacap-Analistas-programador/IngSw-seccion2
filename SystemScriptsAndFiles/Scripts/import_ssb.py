import os
import sys
import MySQLdb

def main():
    dump_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.getcwd(), 'ssb.sql')
    host = os.environ.get('HOST', '127.0.0.1')
    user = os.environ.get('USER', 'root')
    password = os.environ.get('PASSWORD_DB', '')
    port = int(os.environ.get('PORT', '3306'))
    dbname = os.environ.get('DATABASE', 'ssb')

    if not os.path.exists(dump_path):
        print(f"SQL dump not found: {dump_path}")
        sys.exit(1)

    print(f"Connecting to MySQL {host}:{port} as {user}...")
    conn = MySQLdb.connect(host=host, user=user, passwd=password, port=port)
    conn.autocommit(False)
    cur = conn.cursor()

    print(f"Ensuring database '{dbname}' exists...")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    cur.execute(f"USE `{dbname}`;")

    print(f"Importing dump from {dump_path} ... this can take a while")
    with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
        sql = f.read()

    # Naive split by ; at EOL; handles typical dumps without routines
    statements = []
    buff = []
    for line in sql.splitlines():
        line_strip = line.strip()
        # skip full-line comments
        if not line_strip or line_strip.startswith('--'):
            continue
        buff.append(line)
        if line_strip.endswith(';'):
            statements.append('\n'.join(buff))
            buff = []
    if buff:
        statements.append('\n'.join(buff))

    total = len(statements)
    print(f"Executing {total} statements...")
    for i, stmt in enumerate(statements, start=1):
        try:
            cur.execute(stmt)
        except Exception as e:
            print(f"Error at statement {i}: {e}\nStatement:\n{stmt[:500]}...\n")
            conn.rollback()
            raise
        if i % 200 == 0:
            conn.commit()
            print(f"Committed {i}/{total}...")
    conn.commit()
    print("Import completed successfully.")

if __name__ == '__main__':
    main()
