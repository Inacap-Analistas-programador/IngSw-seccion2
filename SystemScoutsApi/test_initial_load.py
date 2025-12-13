
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ApiCoreScouts.Models.mantenedor_model import Rol, Rama, Grupo
from ApiCoreScouts.Models.persona_model import Persona

def test_endpoints():
    client = APIClient()
    User = get_user_model()
    
    # Authenticate
    user = User.objects.first()
    if not user:
        print("Creating temp user for test...")
        user = User.objects.create_superuser('admin_test', 'admin@test.com', 'password')
    
    client.force_authenticate(user=user)
    print(f"Authenticated as {user.usu_username}")

    # 1. Test Personas List
    print("\n--- Testing Personas List ---")
    response_personas = client.get('/api/personas/personas/')
    if response_personas.status_code == 200:
        count = len(response_personas.data.get('results', response_personas.data)) if isinstance(response_personas.data, dict) else len(response_personas.data)
        print(f"✅ /api/personas/personas/ returned 200 OK. Count: {count}")
    else:
        print(f"❌ /api/personas/personas/ failed: {response_personas.status_code}")
        print(response_personas.data)

    # 2. Test Mantenedores: Rol (Singular)
    print("\n--- Testing Mantenedores: Rol ---")
    response_roles = client.get('/api/mantenedores/rol/')
    if response_roles.status_code == 200:
        print(f"✅ /api/mantenedores/rol/ returned 200 OK. Count: {len(response_roles.data)}")
        if len(response_roles.data) == 0:
             print("⚠️ Warning: Roles list is empty. Frontend dropdown will be empty.")
    else:
        print(f"❌ /api/mantenedores/rol/ failed: {response_roles.status_code}")

    # 3. Test Mantenedores: Rama
    print("\n--- Testing Mantenedores: Rama ---")
    response_ramas = client.get('/api/mantenedores/rama/')
    if response_ramas.status_code == 200:
        print(f"✅ /api/mantenedores/rama/ returned 200 OK. Count: {len(response_ramas.data)}")
    else:
        print(f"❌ /api/mantenedores/rama/ failed: {response_ramas.status_code}")

    # 4. Test Mantenedores: Grupo
    print("\n--- Testing Mantenedores: Grupo ---")
    response_grupos = client.get('/api/mantenedores/grupo/')
    if response_grupos.status_code == 200:
        print(f"✅ /api/mantenedores/grupo/ returned 200 OK. Count: {len(response_grupos.data)}")
    else:
        print(f"❌ /api/mantenedores/grupo/ failed: {response_grupos.status_code}")

if __name__ == "__main__":
    test_endpoints()
