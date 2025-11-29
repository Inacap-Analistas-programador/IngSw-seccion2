from ..Models.curso_model import *
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from ..Serializers import Curso_serializer as MC_S
from ..Filters import curso_filter as CF
from rest_framework.permissions import AllowAny

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all().order_by('CUR_ESTADO', 'CUR_DESCRIPCION')
    serializer_class = MC_S.CursoSerializer
    filterset_class = CF.CursoFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = {
        'list': ('PEA_CONSULTAR',),
        'retrieve': ('PEA_CONSULTAR',),
        'create': ('PEA_INGRESAR',),
        'update': ('PEA_MODIFICAR',),
        'partial_update': ('PEA_MODIFICAR',),
        'destroy': ('PEA_ELIMINAR',),
    }

class CursoCuotaViewSet(viewsets.ModelViewSet):
    queryset = Curso_Cuota.objects.all().order_by('CUU_FECHA', 'CUU_ID')
    serializer_class = MC_S.CursoCuotaSerializer
    filterset_class = CF.CursoCuotaFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS

class CursoFechaViewSet(viewsets.ModelViewSet):
    queryset = Curso_Fecha.objects.all()
    serializer_class = MC_S.CursoFechaSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS

class CursoAlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Alimentacion.objects.all().order_by('CUA_FECHA', 'CUA_TIEMPO', 'CUA_ID')
    serializer_class = MC_S.CursoAlimentacionSerializer
    filterset_class = CF.CursoAlimentacionFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS

class CursoCoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Coordinador.objects.all().order_by('CUC_ID')
    serializer_class = MC_S.CursoCoordinadorSerializer
    filterset_class = CF.CursoCoordinadorFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS

class CursoSeccionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Seccion.objects.all().order_by('CUS_SECCION', 'CUS_ID')
    serializer_class = MC_S.CursoSeccionSerializer
    filterset_class = CF.CursoSeccionFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS

class CursoFormadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Formador.objects.all().order_by('CUF_ID')
    serializer_class = MC_S.CursoFormadorSerializer
    filterset_class = CF.CursoFormadorFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS