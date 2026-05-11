import pymysql
import sys

def check_connection():
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            port=3306
        )
        print("SUCCESS: Connected to MySQL server")
        
        # Check if DB exists
        with conn.cursor() as cursor:
            cursor.execute("SHOW DATABASES LIKE 'ssb'")
            result = cursor.fetchone()
            if result:
                print("SUCCESS: Database 'ssb' exists")
            else:
                print("WARNING: Database 'ssb' does NOT exist")
                
        conn.close()
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    check_connection()
