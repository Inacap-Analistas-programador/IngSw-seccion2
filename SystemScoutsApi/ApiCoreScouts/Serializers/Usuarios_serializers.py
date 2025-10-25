from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from ..Models.ModuloUsuarios import *

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Agregar claims personalizados al token
        token['USU_ID'] = user.USU_ID
        token['USU_USERNAME'] = user.USU_USERNAME
        token['PEL_ID'] = user.PEL_ID.PEL_ID
        token['PEL_DESCRIPCION'] = user.PEL_ID.PEL_DESCRIPCION
        
        # Obtener permisos del usuario
        try:
            permisos = Perfil_Aplicacion.objects.filter(
                PEL_ID=user.PEL_ID,
                APL_ID__APL_VIGENTE=True
            ).select_related('APL_ID')
            
            token['permisos'] = [
                {
                    'APL_ID': permiso.APL_ID.APL_ID,
                    'APL_DESCRIPCION': permiso.APL_ID.APL_DESCRIPCION,
                    'PEA_INGRESAR': permiso.PEA_INGRESAR,
                    'PEA_MODIFICAR': permiso.PEA_MODIFICAR,
                    'PEA_ELIMINAR': permiso.PEA_ELIMINAR,
                    'PEA_CONSULTAR': permiso.PEA_CONSULTAR,
                }
                for permiso in permisos
            ]
        except:
            token['permisos'] = []

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Agregar datos extra a la respuesta del token
        data.update({
            'USU_ID': self.user.USU_ID,
            'USU_USERNAME': self.user.USU_USERNAME,
            'PEL_ID': self.user.PEL_ID.PEL_ID,
            'PEL_DESCRIPCION': self.user.PEL_ID.PEL_DESCRIPCION,
            'USU_RUTA_FOTO': self.user.USU_RUTA_FOTO,
            'permisos': self.user.permisos if hasattr(self.user, 'permisos') else []
        })
        
        return data

# Serializer para el modelo Usuario
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