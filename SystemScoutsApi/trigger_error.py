import urllib.request
import urllib.error
import json

base_url = "http://127.0.0.1:8000"

def get_token():
    url = f"{base_url}/login/"
    data = json.dumps({"usu_username": "admin", "password": "admin123"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get('access')
    except urllib.error.HTTPError as e:
        print(f"Login failed: {e}")
        print(e.read().decode('utf-8'))
        return None
    except Exception as e:
        print(f"Login failed: {e}")
        return None

token = get_token()
if not token:
    print("Could not get token, aborting.")
    exit(1)

print(f"Got token: {token[:10]}...")
url = f"{base_url}/api/personas/cursos/"
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})

try:
    print(f"Fetching {url}...")
    with urllib.request.urlopen(req) as response:
        print("Success (200)")
        print(response.read().decode('utf-8')[:500])
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    error_content = e.read().decode('utf-8')
    with open('error_log.html', 'w', encoding='utf-8') as f:
        f.write(error_content)
    try:
        print(json.dumps(json.loads(error_content), indent=2))
    except:
        print(error_content[:1000]) # Print first 1000 chars
except Exception as e:
    print(f"Error: {e}")
