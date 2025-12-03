import os
import django
import sys
import json

# Add the project directory to the sys.path
sys.path.append(os.getcwd())

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')

print("1. Setting up Django...")
try:
    django.setup()
    print("   Django setup successful!")
except Exception as e:
    print(f"   ERROR: Django setup failed: {e}")
    sys.exit(1)

print("\n2. Testing Custom Serializer Token Generation...")
try:
    from ApiCoreScouts.Models.usuario_model import Usuario
    from ApiCoreScouts.Serializers.Usuario_serializer import MyTokenObtainPairSerializer
    
    user = Usuario.objects.first()
    if not user:
        print("   No users found.")
        sys.exit(0)
        
    print(f"   User found: {user.usu_username}")
    
    print("   Calling MyTokenObtainPairSerializer.get_token(user)...")
    try:
        # This calls the custom get_token method which builds the profile payload
        token = MyTokenObtainPairSerializer.get_token(user)
        print("   Token object created successfully.")
        
        print("   Inspecting custom claims in payload...")
        payload = token.payload
        print(f"   Payload keys: {list(payload.keys())}")
        
        if 'perfil' in payload:
            print("   'perfil' claim present.")
        else:
            print("   WARNING: 'perfil' claim MISSING.")
            
        if 'aplicaciones' in payload:
            print(f"   'aplicaciones' claim present. Count: {len(payload['aplicaciones'])}")
        else:
            print("   WARNING: 'aplicaciones' claim MISSING.")

        print("   Attempting to JSON dump the payload (simulating response)...")
        # This will fail if any object in the payload is not serializable (e.g. Decimal, bytes)
        json_payload = json.dumps(payload)
        print("   Payload serialization successful!")
        
    except Exception as e:
        print(f"   ERROR during custom token generation: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nDone.")
