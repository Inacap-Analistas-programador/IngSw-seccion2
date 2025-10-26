from rest_framework import serializers
from ..Models.ModuloUsuarios import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['USU_ID', 'PEL_ID', 'USU_USERNAME', 'USU_PASSWORD', 'USU_RUTA_FOTO', 'USU_VIGENTE']
        extra_kwargs = {
            'USU_PASSWORD': {'write_only': True}
        }

class AplicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aplicacion
        fields = '__all__'
               
class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'

class PerfilAplicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil_Aplicacion
        fields = '__all__'