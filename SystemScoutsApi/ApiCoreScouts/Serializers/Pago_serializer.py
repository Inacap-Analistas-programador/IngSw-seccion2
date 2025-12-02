from rest_framework import serializers
from ..Models.pago_model import *
from .Persona_serializer import PersonaSerializer
from .Curso_serializer import CursoSerializer

class ProveedorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Proveedor
            fields = '__all__'

class ComprobantePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante_Pago
        fields = '__all__'
    
class PagoComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago_Comprobante
        fields = '__all__'
    
class PagoPersonaSerializer(serializers.ModelSerializer):
    # Nested, read-only representations for convenience in the frontend
    persona = PersonaSerializer(source='per_id', read_only=True)
    curso = CursoSerializer(source='cur_id', read_only=True)

    class Meta:
        model = Pago_Persona
        fields = '__all__'
        # Keep default PK-related fields (per_id, cur_id, usu_id) for writes
        # and expose nested read-only fields (persona, curso) for reads.
    
class PrepagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prepago
        fields = '__all__'