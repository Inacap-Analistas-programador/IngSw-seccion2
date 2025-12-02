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
    queryset = Curso.objects.all().order_by('cur_estado', 'cur_descripcion')
    serializer_class = MC_S.CursoSerializer
    filterset_class = CF.CursoFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = {
        'list': ('pea_consultar',),
        'retrieve': ('pea_consultar',),
        'create': ('pea_ingresar',),
        'update': ('pea_modificar',),
        'partial_update': ('pea_modificar',),
        'destroy': ('pea_eliminar',),
    }

class CursoCuotaViewSet(viewsets.ModelViewSet):
    queryset = Curso_Cuota.objects.all().order_by('cuu_fecha', 'cuu_id')
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
    queryset = Curso_Alimentacion.objects.all().order_by('cua_fecha', 'cua_tiempo', 'cua_id')
    serializer_class = MC_S.CursoAlimentacionSerializer
    filterset_class = CF.CursoAlimentacionFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS

class CursoCoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Coordinador.objects.all().order_by('cuc_id')
    serializer_class = MC_S.CursoCoordinadorSerializer
    filterset_class = CF.CursoCoordinadorFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS

class CursoSeccionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Seccion.objects.all().order_by('cus_seccion', 'cus_id')
    serializer_class = MC_S.CursoSeccionSerializer
    filterset_class = CF.CursoSeccionFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS

class CursoFormadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Formador.objects.all().order_by('cuf_id')
    serializer_class = MC_S.CursoFormadorSerializer
    filterset_class = CF.CursoFormadorFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    APP_NAME = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS