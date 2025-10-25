from rest_framework import serializers
from ..Models.ModuloPersonas import *

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class PersonaGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Grupo
        fields = '__all__'

class PersonaFormadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Formador
        fields = '__all__'

class PersonaIndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Individual
        fields = '__all__'

class PersonaNivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Nivel
        fields = '__all__'

class PersonaCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Curso
        fields = '__all__'

class PersonaEstadoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Estado_Curso
        fields = '__all__'

class PersonaVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Vehiculo
        fields = '__all__'