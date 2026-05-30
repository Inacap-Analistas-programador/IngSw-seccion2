from rest_framework import serializers
from django.contrib.auth.models import Group
from ..Models.perfil_ambito_model import PerfilAmbito, NIVEL_CHOICES, NIVEL_GLOBAL
from ..Models.mantenedor_model import Zona, Distrito, Grupo


class PerfilAmbitoSerializer(serializers.ModelSerializer):
    """
    Serializer para leer y escribir el ámbito geográfico de un Perfil (Group).
    Se usa anidado dentro de la creación/edición de Perfiles.
    """
    zona_descripcion     = serializers.CharField(source='zona.zon_descripcion', read_only=True)
    distrito_descripcion = serializers.CharField(source='distrito.dis_descripcion', read_only=True)
    grupo_descripcion    = serializers.CharField(source='grupo.gru_descripcion', read_only=True)
    nivel_display        = serializers.SerializerMethodField()

    class Meta:
        model = PerfilAmbito
        fields = [
            'nivel', 'nivel_display',
            'zona',     'zona_descripcion',
            'distrito', 'distrito_descripcion',
            'grupo',    'grupo_descripcion',
        ]

    def get_nivel_display(self, obj):
        return dict(NIVEL_CHOICES).get(obj.nivel, obj.nivel)

    def validate(self, data):
        """Delegamos la validación jerárquica al método clean() del modelo."""
        # Construir instancia temporal para ejecutar clean()
        instance = PerfilAmbito(
            nivel=data.get('nivel', NIVEL_GLOBAL),
            zona=data.get('zona'),
            distrito=data.get('distrito'),
            grupo=data.get('grupo'),
        )
        instance.clean()
        return data


class GroupWithAmbitoSerializer(serializers.ModelSerializer):
    """
    Extiende el serializer de Group estándar para incluir el ámbito.
    Usado en el endpoint de Perfiles para configurar restricciones de datos.
    """
    ambito = PerfilAmbitoSerializer(required=False, allow_null=True)
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'ambito']

    def update(self, instance, validated_data):
        ambito_data = validated_data.pop('ambito', None)

        # Actualizar nombre del Group
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Actualizar o crear el PerfilAmbito
        if ambito_data is not None:
            ambito, _ = PerfilAmbito.objects.get_or_create(group=instance)
            for attr, value in ambito_data.items():
                setattr(ambito, attr, value)
            ambito.save()  # Dispara full_clean() internamente

        return instance

    def create(self, validated_data):
        ambito_data = validated_data.pop('ambito', None)
        group = Group.objects.create(**validated_data)

        if ambito_data:
            PerfilAmbito.objects.create(
                group=group,
                nivel=ambito_data.get('nivel', NIVEL_GLOBAL),
                zona=ambito_data.get('zona'),
                distrito=ambito_data.get('distrito'),
                grupo=ambito_data.get('grupo'),
            )
        else:
            # Por defecto crear ámbito global
            PerfilAmbito.objects.create(group=group, nivel=NIVEL_GLOBAL)

        return group
