from ..Models.ModuloCursos import *
from rest_framework import viewsets
from ..Serializers import Cursos_serializers as MC_S

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = MC_S.CursoSerializer

class CursoCuotaViewSet(viewsets.ModelViewSet):
    queryset = Curso_Cuota.objects.all()
    serializer_class = MC_S.CursoCuotaSerializer

class CursoFechaViewSet(viewsets.ModelViewSet):
    queryset = Curso_Fecha.objects.all()
    serializer_class = MC_S.CursoFechaSerializer

class CursoAlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Alimentacion.objects.all()
    serializer_class = MC_S.CursoAlimentacionSerializer

class CursoCoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Coordinador.objects.all()
    serializer_class = MC_S.CursoCoordinadorSerializer

class CursoSeccionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Seccion.objects.all()
    serializer_class = MC_S.CursoSeccionSerializer

class CursoFormadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Formador.objects.all()
    serializer_class = MC_S.CursoFormadorSerializer