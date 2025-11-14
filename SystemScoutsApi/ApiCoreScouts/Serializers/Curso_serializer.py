from rest_framework import serializers
from ..Models.curso_model import *

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class CursoCuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Cuota
        fields = '__all__'

class CursoFechaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Fecha
        fields = '__all__'

class CursoAlimentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Alimentacion
        fields = '__all__'

class CursoCoordinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Coordinador
        fields = '__all__'

class CursoSeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Seccion
        fields = '__all__'

class CursoFormadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Formador
        fields = '__all__'