from rest_framework import serializers
from ..Models.ModuloPagos import *
from ..Serializers.Personas_serializers import PersonaSerializer
from ..Serializers.Cursos_serializers import CursoSerializer

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
    persona = PersonaSerializer(source='PER_ID', read_only=True)
    curso = CursoSerializer(source='CUR_ID', read_only=True)

    class Meta:
        model = Pago_Persona
        fields = '__all__'
        # Keep default PK-related fields (PER_ID, CUR_ID, USU_ID) for writes
        # and expose nested read-only fields (persona, curso) for reads.
    
class PrepagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prepago
        fields = '__all__'