from rest_framework import serializers
from ..Models.ModuloUsuarios import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'USU_USERNAME'

    def validate(self, attrs):
        username = attrs.get('USU_USERNAME')
        password = attrs.get('password')

        try:
            user = Usuario.objects.get(USU_USERNAME=username)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado")

        if not user.check_password(password):
            raise serializers.ValidationError("Contraseña incorrecta")

        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo")

        data = super().validate({'username': username, 'password': password})
        data['USU_USERNAME'] = user.USU_USERNAME  # opcional: devolverlo en el token
        return data   

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['USU_ID', 'PEL_ID', 'USU_USERNAME', 'USU_RUTA_FOTO', 'USU_VIGENTE']
        read_only_fields = ('USU_ID',)

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