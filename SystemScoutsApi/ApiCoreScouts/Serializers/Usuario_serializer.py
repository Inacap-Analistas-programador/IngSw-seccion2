from rest_framework import serializers
from ..Models.usuario_model import Usuario
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'
    # Aceptar ambos nombres en el payload para compatibilidad (frontend puede enviar 'username' o 'usu_username')
    username = serializers.CharField(write_only=True, required=False)
    usu_username = serializers.CharField(write_only=True, required=False)

    @staticmethod
    def _build_perms_payload(user):
        """Arma los datos de grupos y permisos."""
        grupos = []
        for group in user.groups.all():
            grupos.append({
                'id': group.id,
                'nombre': group.name
            })

        # Mapeamos los permisos de Django al formato que el frontend espera
        aplicaciones = {} # app_label -> { permisos }
        
        # Django permissions are 'app.view_model', 'app.add_model', etc.
        for perm in user.get_all_permissions():
            try:
                app_label, codename = perm.split('.')
                # codename is usually 'action_model'
                parts = codename.split('_')
                if len(parts) >= 2:
                    action = parts[0]
                    model = "_".join(parts[1:])
                    
                    if model not in aplicaciones:
                        aplicaciones[model] = {
                            'apl_descripcion': model.capitalize(),
                            'permisos': {
                                'pea_ingresar': False,
                                'pea_modificar': False,
                                'pea_eliminar': False,
                                'pea_consultar': False,
                            }
                        }
                    
                    if action == 'view': aplicaciones[model]['permisos']['pea_consultar'] = True
                    elif action == 'add': aplicaciones[model]['permisos']['pea_ingresar'] = True
                    elif action == 'change': aplicaciones[model]['permisos']['pea_modificar'] = True
                    elif action == 'delete': aplicaciones[model]['permisos']['pea_eliminar'] = True
            except ValueError:
                continue

        # Convertimos a lista para compatibilidad
        aplicaciones_list = []
        for model, data in aplicaciones.items():
            aplicaciones_list.append({
                'apl_id': model, # Usamos el nombre del modelo como ID string
                'apl_descripcion': data['apl_descripcion'],
                'permisos': data['permisos']
            })

        return grupos, aplicaciones_list

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        grupos, aplicaciones = cls._build_perms_payload(user)

        token['usu_id'] = int(user.usu_id)
        token['usu_username'] = user.username
        token['usu_vigente'] = user.is_active
        token['grupos'] = grupos
        token['aplicaciones'] = aplicaciones
        
        # Para compatibilidad con frontend que busca 'perfil'
        if grupos:
            token['perfil'] = {
                'pel_id': grupos[0]['id'],
                'pel_descripcion': grupos[0]['nombre'],
                'pel_vigente': True
            }
        else:
            token['perfil'] = None

        return token

    def validate(self, attrs):
        # Compatibilidad: permitir que el cliente envíe 'username' o 'usu_username'
        if self.username_field not in attrs and 'usu_username' in attrs:
            attrs[self.username_field] = attrs.get('usu_username')
        elif self.username_field not in attrs and 'username' in attrs:
            attrs[self.username_field] = attrs.get('username')

        data = super().validate(attrs)
        user = self.user
        grupos, aplicaciones = self._build_perms_payload(user)

        data.update({
            'usu_id': int(user.usu_id),
            'usu_username': user.username,
            'usu_vigente': user.is_active,
            'grupos': grupos,
            'aplicaciones': aplicaciones,
        })
        
        if grupos:
            data['perfil'] = {
                'id': grupos[0]['id'],
                'nombre': grupos[0]['nombre']
            }
            
        return data

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_null=True, min_length=8)
    # Grupos (roles)
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 
            'email', 'is_active', 'password',
            'is_staff', 'is_superuser', 'groups'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        groups_data = validated_data.pop('groups', [])
        
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        
        if groups_data:
            user.groups.set(groups_data)
            
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        groups_data = validated_data.pop('groups', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
            
        if groups_data is not None:
            instance.groups.set(groups_data)
            
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']

