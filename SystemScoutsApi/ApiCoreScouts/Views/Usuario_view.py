from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..Serializers import (
    UsuarioSerializer, 
    GroupSerializer, 
    PermissionSerializer, 
    MyTokenObtainPairSerializer
)
from ..Models.usuario_model import Usuario
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Permissions import PerfilPermission
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Vista de login personalizada que usa MyTokenObtainPairSerializer.
    """
    serializer_class = MyTokenObtainPairSerializer


import logging

logger = logging.getLogger(__name__)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Usuarios'


    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f'Exception in UsuarioViewSet.list: {str(e)}', exc_info=True)
            from rest_framework.response import Response
            from rest_framework import status
            return Response({'detail': 'internal_server_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    app_name = 'Perfiles'

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    app_name = 'Permisos'



