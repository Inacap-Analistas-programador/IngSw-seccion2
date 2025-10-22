from rest_framework import viewsets
from ApiCore.serializers import ModuloCursosSerializers
from .models import (Curso, Curso_Cuota, Curso_Fecha, Curso_Alimentacion,
                     Curso_Coordinador, Curso_Seccion, Curso_Formador, Tipo_Curso)

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = ModuloCursosSerializers.CursoSerializer

class CursoCuotaViewSet(viewsets.ModelViewSet):
    queryset = Curso_Cuota.objects.all()
    serializer_class = ModuloCursosSerializers.CursoCuotaSerializer

class CursoFechaViewSet(viewsets.ModelViewSet):
    queryset = Curso_Fecha.objects.all()
    serializer_class = ModuloCursosSerializers.CursoFechaSerializer

class CursoAlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Alimentacion.objects.all()
    serializer_class = ModuloCursosSerializers.CursoAlimentacionSerializer

class CursoCoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Coordinador.objects.all()
    serializer_class = ModuloCursosSerializers.CursoCoordinadorSerializer

class CursoSeccionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Seccion.objects.all()
    serializer_class = ModuloCursosSerializers.CursoSeccionSerializer

class CursoFormadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Formador.objects.all()
    serializer_class = ModuloCursosSerializers.CursoFormadorSerializer

class TipoCursoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Curso.objects.all()
    serializer_class = ModuloCursosSerializers.TipoCursoSerializer
