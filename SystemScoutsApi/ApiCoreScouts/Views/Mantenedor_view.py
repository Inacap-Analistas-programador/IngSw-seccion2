from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..Serializers import Mantenedor_serializer as MP_S
from ..Models.mantenedor_model import *
from ..Models.mantenedor_model import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Permissions import PerfilPermission
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from ..Filters import mantenedor_filter as MP_F

BASE_ACTION_PERMISSIONS = {
    'list': ('pea_consultar',),
    'retrieve': ('pea_consultar',),
    'create': ('pea_ingresar',),
    'update': ('pea_modificar',),
    'partial_update': ('pea_modificar',),
    'destroy': ('pea_eliminar',),
}

class ConceptoViewSet(viewsets.ModelViewSet):
    queryset = Concepto_Contable.objects.all()
    serializer_class = MP_S.ConceptoContableSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.ConceptoContableFilter
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = MP_S.RolSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.RolFilter
    APP_NAME = "Mantenedores"

    @action(detail=False, methods=['get'])
    def min(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.values('ROL_ID', 'ROL_NOMBRE')
        results = [{'id': item['ROL_ID'], 'nombre': item['ROL_NOMBRE']} for item in data]
        return Response({'results': results})

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = MP_S.CargoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.CargoFilter
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class RamaViewSet(viewsets.ModelViewSet):
    queryset = Rama.objects.all()
    serializer_class = MP_S.RamaSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.RamaFilter
    APP_NAME = "Mantenedores"

    @action(detail=False, methods=['get'])
    def min(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.values('RAM_ID', 'RAM_DESCRIPCION')
        results = [{'id': item['RAM_ID'], 'nombre': item['RAM_DESCRIPCION']} for item in data]
        return Response({'results': results})

class EstadoCivilViewSet(viewsets.ModelViewSet):
    queryset = Estado_Civil.objects.all()
    serializer_class = MP_S.EstadoCivilSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.EstadoCivilFilter
    APP_NAME = "Mantenedores"

class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = MP_S.NivelSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.NivelFilter
    APP_NAME = "Mantenedores"

class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = MP_S.ZonaSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.ZonaFilter
    APP_NAME = "Mantenedores"

class DistritoViewSet(viewsets.ModelViewSet):
    queryset = Distrito.objects.all()
    serializer_class = MP_S.DistritoSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.DistritoFilter
    APP_NAME = "Mantenedores"

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = MP_S.GrupoSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.GrupoFilter
    APP_NAME = "Mantenedores"

    @action(detail=False, methods=['get'])
    def min(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.values('GRU_ID', 'GRU_DESCRIPCION')
        results = [{'id': item['GRU_ID'], 'nombre': item['GRU_DESCRIPCION']} for item in data]
        return Response({'results': results})

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = MP_S.RegionSerializer    
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.RegionFilter
    APP_NAME = "Mantenedores"

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = MP_S.ProvinciaSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.ProvinciaFilter
    APP_NAME = "Mantenedores"

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = MP_S.ComunaSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.ComunaFilter
    APP_NAME = "Mantenedores"

class TipoCursoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Curso.objects.all()
    serializer_class = MP_S.TipoCursoSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.TipoCursoFilter
    APP_NAME = "Mantenedores"

class TipoArchivoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Archivo.objects.all()
    serializer_class = MP_S.TipoArchivoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.TipoArchivoFilter
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class AlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Alimentacion.objects.all()
    serializer_class = MP_S.AlimentacionSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MP_F.AlimentacionFilter
    APP_NAME = "Mantenedores"
