from rest_framework import serializers
from ..Models.archivo_model import *

class ArchivoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Archivo
            fields = '__all__'

class ArchivoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo_Curso
        fields = '__all__'

class ArchivoPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo_Persona
        fields = '__all__'