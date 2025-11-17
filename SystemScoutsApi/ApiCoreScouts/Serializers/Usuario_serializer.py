from rest_framework import serializers
from ..Models.ModuloUsuarios import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'USU_USERNAME'

    @staticmethod
    def _build_perfil_payload(perfil):
        """
        Arma los datos de perfil y permisos.

        No es estrictamente necesario usar un helper, pero mantener la
        construcción en un solo lugar evita duplicar lógica entre
        ``get_token`` y ``validate`` y asegura que ambos devuelvan la misma
        información.
        """
        if not perfil:
            return None, []

        aplicaciones = []
        for perfil_aplicacion in (
            perfil.perfil_aplicacion_set.select_related('APL_ID').all()
        ):
            app = perfil_aplicacion.APL_ID
            aplicaciones.append({
                'APL_ID': app.APL_ID,
                'APL_DESCRIPCION': app.APL_DESCRIPCION,
                'APL_VIGENTE': app.APL_VIGENTE,
                'permisos': {
                    'PEA_INGRESAR': perfil_aplicacion.PEA_INGRESAR,
                    'PEA_MODIFICAR': perfil_aplicacion.PEA_MODIFICAR,
                    'PEA_ELIMINAR': perfil_aplicacion.PEA_ELIMINAR,
                    'PEA_CONSULTAR': perfil_aplicacion.PEA_CONSULTAR,
                },
            })

        perfil_payload = {
            'PEL_ID': perfil.PEL_ID,
            'PEL_DESCRIPCION': getattr(perfil, 'PEL_DESCRIPCION', None),
            'PEL_VIGENTE': getattr(perfil, 'PEL_VIGENTE', None),
        }
        return perfil_payload, aplicaciones

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        perfil_payload, aplicaciones = cls._build_perfil_payload(getattr(user, 'PEL_ID', None))

        token['USU_ID'] = user.USU_ID
        token['USU_USERNAME'] = user.USU_USERNAME
        token['USU_VIGENTE'] = user.USU_VIGENTE
        token['perfil'] = perfil_payload
        token['aplicaciones'] = aplicaciones

        return token

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

        credentials = {self.username_field: username, 'password': password}
        data = super().validate(credentials)

        perfil_payload, aplicaciones = self._build_perfil_payload(getattr(user, 'PEL_ID', None))

        data.update({
            'USU_ID': user.USU_ID,
            'USU_USERNAME': user.USU_USERNAME,
            'USU_VIGENTE': user.USU_VIGENTE,
            'perfil': perfil_payload,
            'aplicaciones': aplicaciones,
        })
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