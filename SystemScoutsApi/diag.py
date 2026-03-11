from ApiCoreScouts.Models.persona_model import Persona, Persona_Curso
from ApiCoreScouts.Models.mantenedor_model import Alimentacion
from ApiCoreScouts.Serializers.Persona_serializer import PersonaCompletaSerializer
import os
import django

def test():
    try:
        p = Persona.objects.get(per_id=167)
        ser = PersonaCompletaSerializer(p)
        print("### FULL SERIALIZER DATA ###")
        for k in sorted(ser.data.keys()):
            print(f"{k}: {ser.data[k]}")
    except Exception as e:
        print(f"### ERROR: {e}")

if __name__ == "__main__":
    test()
