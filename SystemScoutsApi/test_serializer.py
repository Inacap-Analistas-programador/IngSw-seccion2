import sys
import os
import django

sys.path.append(r"d:\IngSw-seccion2\SystemScoutsApi")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SystemScoutsApi.settings")
django.setup()

from ApiCoreScouts.Models.persona_model import Persona
from ApiCoreScouts.Serializers.Persona_serializer import PersonaCompletaSerializer

p = Persona.objects.first()
if p:
    serializer = PersonaCompletaSerializer(p)
    print(serializer.data)
else:
    print("No personas found")
