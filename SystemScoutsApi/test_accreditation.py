import os
import django
import json

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from ApiCoreScouts.Views.Persona_view import PersonaViewSet
from ApiCoreScouts.Models.persona_model import Persona
from ApiCoreScouts.Models.usuario_model import Usuario

def test_accreditation():
    print("Testing accreditation endpoint...")
    
    # 1. Get a Person
    # Use Luis or anyone
    person = Persona.objects.filter(per_nombres__icontains="Luis").first()
    if not person:
        person = Persona.objects.first()
    
    if not person:
        print("No person found to test.")
        return

    print(f"Testing with Person: {person.per_nombres} (ID: {person.per_id})")

    # Ensure enrollment exists
    from ApiCoreScouts.Models.persona_model import Persona_Curso
    from ApiCoreScouts.Models.curso_model import Curso_Seccion
    
    pec = Persona_Curso.objects.filter(per_id=person).first()
    if not pec:
        print("Person not enrolled. Enrolling in default section...")
        seccion = Curso_Seccion.objects.first()
        if not seccion:
            print("No course sections available. Cannot enroll.")
            return
            
        from ApiCoreScouts.Models.mantenedor_model import Rol, Nivel, Alimentacion
        # defaults
        rol = Rol.objects.first()
        nivel = Nivel.objects.first()
        ali = Alimentacion.objects.first()
        
        pec = Persona_Curso.objects.create(
            per_id=person,
            cus_id=seccion,
            rol_id=rol,
            niv_id=nivel,
            ali_id=ali,
            pec_registro=False,
            pec_acreditacion=False,
            pec_envio_correo_qr=False
        )
        print("Enrolled successfully.")

    # 2. Setup Request
    factory = APIRequestFactory()
    url = f'/api/personas/personas/acreditacion_manual_acreditar/'
    payload = {'per_id': person.per_id, 'rut': person.per_run}
    
    request = factory.post(url, payload, format='json')
    
    # 3. Authenticate
    user = Usuario.objects.first()
    force_authenticate(request, user=user)

    # 4. Call View
    # Note: ViewSet methods are bound to actions. 
    # For a custom @action, we need to bind it properly.
    view = PersonaViewSet.as_view({'post': 'acreditacion_manual_acreditar'})
    
    try:
        response = view(request)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success! Response data keys:", list(response.data.keys()))
            # Check if acreditated
            print(f"Acreditado: {response.data.get('pec_acreditado')}")
            # Note: The serializer returns 'pec_acreditado' (aliased from pec_acreditacion in serializer)
            # or it might return the whole object where we need to check fields.
            # In PersonaCompletaSerializer: pec_acreditado = BooleanField(source='pec_acreditacion')
        else:
            print("Error Response:", response.data)
            
    except Exception as e:
        print(f"Exception calling view: {e}")

if __name__ == "__main__":
    test_accreditation()
