
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
# Force DEBUG=True for the script environment too, just in case
os.environ['DJANGO_DEBUG'] = 'True'
django.setup()

# Patch ALLOWED_HOSTS
settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver', 'localhost', '127.0.0.1']

from rest_framework.test import APIClient
from ApiCoreScouts.Models.security_model import SL

def verify_security():
    client = APIClient()
    username = 'admin'
    password_correct = 'DgHj343@34w3!!q' 
    password_wrong = 'wrongpassword'

    print("--- 1. Testing Successful Login ---")
    response = client.post('/login/', {'usu_username': username, 'password': password_correct}, format='json')
    if response.status_code == 200:
        print("Login Success: OK")
    else:
        print(f"Login Success FAILED: {response.status_code}")
        print(response.content.decode('utf-8')[:200])

if __name__ == "__main__":
    verify_security()
