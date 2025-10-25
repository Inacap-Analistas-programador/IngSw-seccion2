from rest_framework import serializers
from ..Models.ModuloPagos import *

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
    class Meta:
        model = Pago_Persona
        fields = '__all__'
    
class PrepagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prepago
        fields = '__all__'