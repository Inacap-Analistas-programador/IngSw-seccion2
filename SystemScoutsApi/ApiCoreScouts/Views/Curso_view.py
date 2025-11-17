from ..Models.curso_model import *
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from ..Serializers import Curso_serializer as MC_S
from ..Filters import curso_filter as CF

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

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
    filterset_class = CF.CursoAlimentacionFilter
    pagination_class = StandardResultsSetPagination

class CursoCoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Coordinador.objects.all()
    serializer_class = MC_S.CursoCoordinadorSerializer

class CursoSeccionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Seccion.objects.all()
    serializer_class = MC_S.CursoSeccionSerializer

class CursoFormadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Formador.objects.all()
    serializer_class = MC_S.CursoFormadorSerializer
    filterset_class = CF.CursoFormadorFilter
    pagination_class = StandardResultsSetPagination