from rest_framework import serializers
from ..Models.usuario_model import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'USU_USERNAME'

    def validate(self, attrs):
        username = attrs.get(self.username_field) or attrs.get('username')
        password = attrs.get('password')

        errors = {}
        user = None
        try:
            user = Usuario.objects.only('USU_ID', 'USU_USERNAME', 'password', 'USU_VIGENTE').get(USU_USERNAME=username)
        except Usuario.DoesNotExist:
            errors['detail'] = "Usuario no encontrado"

        if user is not None:
            if password is None or not user.check_password(password):
                errors['detail'] = "Contraseña incorrecta"
            elif not user.is_active:
                errors['detail'] = "Usuario inactivo"

        if errors:
            # Always return a dict, even for errors
            raise serializers.ValidationError(errors)

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'USU_USERNAME': user.USU_USERNAME,
        }
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