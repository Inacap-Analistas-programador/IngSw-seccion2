import os
import django
# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from ApiCoreScouts.Views.Persona_view import PersonaViewSet
from ApiCoreScouts.Models.persona_model import Persona

def test_search():
    # First, verify we have data
    count = Persona.objects.count()
    print(f"Total personas in DB: {count}")
    
    if count == 0:
        print("No personas found in database. Search will definitely fail.")
        return

    # Pick a name to search for
    first_person = Persona.objects.first()
    search_term = first_person.per_nombres.split()[0]
    print(f"Testing search for term: '{search_term}' (from person: {first_person.per_nombres})")

    factory = APIRequestFactory()
    # Mock request with ?search=term
    request = factory.get(f'/api/personas/personas/?search={search_term}')
    from rest_framework.test import force_authenticate
    from ApiCoreScouts.Models import Usuario
    
    # Try to find a user or create a dummy one for testing context
    user = Usuario.objects.first()
    if not user:
        print("No user found for auth simulation. Creating temporary one if possible or skipping auth check (might fail).")
    
    view = PersonaViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=user)
    response = view(request)
    
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        import json
        data = response.data
        if hasattr(data, 'get') and 'results' in data:
            results = data['results']
        else:
            results = data if isinstance(data, list) else [data]
            
        print(f"Found {len(results)} results.")
        if len(results) > 0:
            first = results[0]
            print("First result keys:", list(first.keys()))
            print("Full first result:")
            # Use default=str to handle non-serializable objects if any
            print(json.dumps(first, indent=2, default=str))
    else:
        print("Error response:", response.data)

if __name__ == "__main__":
    test_search()
