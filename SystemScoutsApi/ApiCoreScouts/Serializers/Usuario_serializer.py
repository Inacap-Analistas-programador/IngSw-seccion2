from rest_framework import serializers
from ..Models.usuario_model import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'usu_username'
    # Aceptar ambos nombres en el payload para compatibilidad (frontend puede enviar 'username' o 'usu_username')
    username = serializers.CharField(write_only=True, required=False)
    usu_username = serializers.CharField(write_only=True, required=False)

    @staticmethod
    def _build_perfil_payload(perfil):
        """Arma los datos de perfil y permisos.

        No es estrictamente necesario usar un helper, pero mantener la
        construcción en un solo lugar evita duplicar lógica entre
        ``get_token`` y ``validate`` y asegura que ambos devuelvan la misma
        información.
        """
        if not perfil:
            return None, []

        def to_bool(val):
            if isinstance(val, bytes):
                return val == b'\x01'
            return bool(val)

        aplicaciones = []
        for perfil_aplicacion in (
            perfil.perfil_aplicacion_set.select_related('apl_id').all()
        ):
            app = perfil_aplicacion.apl_id
            aplicaciones.append({
                'apl_id': int(app.apl_id),
                'apl_descripcion': app.apl_descripcion,
                'apl_vigente': to_bool(app.apl_vigente),
                'permisos': {
                    'pea_ingresar': to_bool(perfil_aplicacion.pea_ingresar),
                    'pea_modificar': to_bool(perfil_aplicacion.pea_modificar),
                    'pea_eliminar': to_bool(perfil_aplicacion.pea_eliminar),
                    'pea_consultar': to_bool(perfil_aplicacion.pea_consultar),
                },
            })

        perfil_payload = {
            'pel_id': int(perfil.pel_id),
            'pel_descripcion': getattr(perfil, 'pel_descripcion', None),
            'pel_vigente': to_bool(getattr(perfil, 'pel_vigente', None)),
        }
        return perfil_payload, aplicaciones

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Fix: Ensure standard user_id claim is int (not Decimal)
        if 'user_id' in token:
            token['user_id'] = int(token['user_id'])

        perfil_payload, aplicaciones = cls._build_perfil_payload(getattr(user, 'pel_id', None))

        token['usu_id'] = int(user.usu_id)
        token['usu_username'] = user.usu_username
        token['usu_vigente'] = user.usu_vigente == b'\x01' if isinstance(user.usu_vigente, bytes) else user.usu_vigente
        token['perfil'] = perfil_payload
        token['aplicaciones'] = aplicaciones

        return token

    def validate(self, attrs):
        """Delegamos la autenticación en ``super`` y solo enriquecemos la respuesta.

        Añadimos registros adicionales para depuración y soporte para ambos nombres de campo.
        """

        # Compatibilidad: permitir que el cliente envíe 'username' o 'usu_username'
        if self.username_field not in attrs and 'username' in attrs:
            attrs[self.username_field] = attrs.get('username')

        data = super().validate(attrs)
        user = self.user

        perfil_payload, aplicaciones = self._build_perfil_payload(getattr(user, 'pel_id', None))

        data.update({
            'usu_id': int(user.usu_id),
            'usu_username': user.usu_username,
            'usu_vigente': user.usu_vigente == b'\x01' if isinstance(user.usu_vigente, bytes) else user.usu_vigente,
            'perfil': perfil_payload,
            'aplicaciones': aplicaciones,
        })
        return data

class LoginSerializer(serializers.Serializer):
    usu_username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(write_only=True, min_length=3)


class UsuarioSerializer(serializers.ModelSerializer):
    # Permitimos enviar una contraseña al crear/actualizar usuario desde la API
    password = serializers.CharField(write_only=True, required=False, allow_null=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ['usu_id', 'pel_id', 'usu_username', 'usu_email', 'usu_ruta_foto', 'usu_vigente', 'password']
        read_only_fields = ('usu_id',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # Si no se entrega password, generar una contraseña segura aleatoria
        if not password:
            import secrets
            # 12 caracteres alfanuméricos seguros
            password = secrets.token_urlsafe(12)

        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None and password != '':
            instance.set_password(password)
        instance.save()
        return instance


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
