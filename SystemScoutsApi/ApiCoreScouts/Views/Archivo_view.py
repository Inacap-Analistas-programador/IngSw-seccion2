from rest_framework import viewsets
from ..Serializers import Archivo_serializer as MA_S
from ..Models.archivo_model import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Permissions import PerfilPermission

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = MA_S.ArchivoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Archivos"
    ACTION_PERMISSIONS = {
        'list': ('pea_consultar',),
        'retrieve': ('pea_consultar',),
        'create': ('pea_ingresar',),
        'update': ('pea_modificar',),
        'partial_update': ('pea_modificar',),
        'destroy': ('pea_eliminar',),
    }

class ArchivoCursoViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Curso.objects.all()
    serializer_class = MA_S.ArchivoCursoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Archivos"
    ACTION_PERMISSIONS = ArchivoViewSet.ACTION_PERMISSIONS

class ArchivoPersonaViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Persona.objects.all()
    serializer_class = MA_S.ArchivoPersonaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Archivos"
    ACTION_PERMISSIONS = ArchivoViewSet.ACTION_PERMISSIONS
