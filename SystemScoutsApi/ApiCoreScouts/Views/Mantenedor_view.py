from rest_framework import viewsets
from ..Serializers import Mantenedor_serializer as MP_S
from ..Models.mantenedor_model import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Permissions import PerfilPermission

BASE_ACTION_PERMISSIONS = {
    'list': ('PEA_CONSULTAR',),
    'retrieve': ('PEA_CONSULTAR',),
    'create': ('PEA_INGRESAR',),
    'update': ('PEA_MODIFICAR',),
    'partial_update': ('PEA_MODIFICAR',),
    'destroy': ('PEA_ELIMINAR',),
}

class ConceptoViewSet(viewsets.ModelViewSet):
    queryset = Concepto_Contable.objects.all()
    serializer_class = MP_S.ConceptoContableSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = MP_S.RolSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = MP_S.CargoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class RamaViewSet(viewsets.ModelViewSet):
    queryset = Rama.objects.all()
    serializer_class = MP_S.RamaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class EstadoCivilViewSet(viewsets.ModelViewSet):
    queryset = Estado_Civil.objects.all()
    serializer_class = MP_S.EstadoCivilSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = MP_S.NivelSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = MP_S.ZonaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class DistritoViewSet(viewsets.ModelViewSet):
    queryset = Distrito.objects.all()
    serializer_class = MP_S.DistritoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = MP_S.GrupoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = MP_S.RegionSerializer    
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = MP_S.ProvinciaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = MP_S.ComunaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class TipoCursoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Curso.objects.all()
    serializer_class = MP_S.TipoCursoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class TipoArchivoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Archivo.objects.all()
    serializer_class = MP_S.TipoArchivoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS

class AlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Alimentacion.objects.all()
    serializer_class = MP_S.AlimentacionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Mantenedores"
    ACTION_PERMISSIONS = BASE_ACTION_PERMISSIONS
