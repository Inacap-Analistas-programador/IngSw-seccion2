from rest_framework import serializers
from ..Models.usuario_model import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'USU_USERNAME'
    # Aceptar ambos nombres en el payload para compatibilidad (frontend puede enviar 'username' o 'USU_USERNAME')
    username = serializers.CharField(write_only=True, required=False)
    USU_USERNAME = serializers.CharField(write_only=True, required=False)

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
        """Delegamos la autenticación en ``super`` y solo enriquecemos la respuesta.

        Añadimos registros adicionales para depuración y soporte para ambos nombres de campo.
        """

        # Compatibilidad: permitir que el cliente envíe 'username' o 'USU_USERNAME'
        if self.username_field not in attrs and 'username' in attrs:
            attrs[self.username_field] = attrs.get('username')

        # Registrar intento de login para ayudar a debug (se imprimirá en la consola del servidor)
        try:
            uname = attrs.get(self.username_field)
            # evitar imprimir contraseñas en logs
            print(f"[Auth] Login attempt for username={uname!r}")
        except Exception:
            pass

        # Intentar autenticar manualmente para obtener más información en logs
        try:
            from django.contrib.auth import authenticate
            uname = attrs.get(self.username_field)
            pwd = attrs.get('password')
            auth_user = authenticate(username=uname, password=pwd)
            print(f"[Auth] authenticate() returned: {auth_user!r}")
            if auth_user is None:
                # inspeccionar posible causa
                try:
                    u = Usuario.objects.get(USU_USERNAME=uname)
                    print(f"[Auth] Found user USU_VIGENTE={u.USU_VIGENTE}, password_hash={u.password[:60]}...")
                    try:
                        print(f"[Auth] check_password => {u.check_password(pwd)}")
                    except Exception as e:
                        print('[Auth] error checking password:', e)
                except Usuario.DoesNotExist:
                    print('[Auth] user does not exist')
        except Exception as e:
            print('[Auth] error during manual authenticate debug:', e)

        data = super().validate(attrs)
        user = self.user

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
    USU_USERNAME = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(write_only=True, min_length=3)


class UsuarioSerializer(serializers.ModelSerializer):
    # Permitimos enviar una contraseña al crear/actualizar usuario desde la API
    password = serializers.CharField(write_only=True, required=False, allow_null=True, min_length=3)
    # Devolver la contraseña generada en la respuesta cuando se crea un usuario
    raw_password = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Usuario
        fields = ['USU_ID', 'PEL_ID', 'USU_USERNAME', 'USU_RUTA_FOTO', 'USU_VIGENTE', 'password', 'raw_password']
        read_only_fields = ('USU_ID', 'raw_password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # Si no se entrega password, generar una contraseña segura aleatoria
        if not password:
            import secrets
            # 12 caracteres alfanuméricos seguros
            password = secrets.token_urlsafe(9)

        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        # Guardar la contraseña en una propiedad temporal para exponerla en la respuesta
        setattr(usuario, '_raw_password', password)
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None and password != '':
            instance.set_password(password)
        instance.save()
        return instance

    def get_raw_password(self, obj):
        return getattr(obj, '_raw_password', None)


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
