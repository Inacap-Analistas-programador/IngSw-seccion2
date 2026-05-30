from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..Serializers import (
    UsuarioSerializer,
    GroupSerializer,
    PermissionSerializer,
    MyTokenObtainPairSerializer,
    PerfilAmbitoSerializer,
    GroupWithAmbitoSerializer,
)
from ..Models.usuario_model import Usuario
from ..Models.perfil_ambito_model import PerfilAmbito, NIVEL_CHOICES
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
            return Response({'detail': 'internal_server_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    app_name = 'Perfiles'

# App labels internas de Django que no deben exponerse en el gestor de perfiles
_INTERNAL_APP_LABELS = {'admin', 'auth', 'contenttypes', 'sessions'}

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.exclude(
        content_type__app_label__in=_INTERNAL_APP_LABELS
    ).select_related('content_type')
    serializer_class = PermissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    app_name = 'Permisos'


class GroupWithAmbitoViewSet(viewsets.ModelViewSet):
    """
    ViewSet que expone los Perfiles (Group) con su PerfilAmbito anidado.
    Usado por Roles.vue para configurar el nivel de acceso geográfico de cada perfil.

    GET  /api/perfiles-ambito/          → Lista todos los perfiles con su ámbito
    GET  /api/perfiles-ambito/{id}/     → Detalle de un perfil con ámbito
    PUT  /api/perfiles-ambito/{id}/     → Actualizar perfil + ámbito
    POST /api/perfiles-ambito/          → Crear perfil con ámbito
    GET  /api/perfiles-ambito/niveles/  → Lista de niveles disponibles (para selectores)
    """
    queryset = Group.objects.prefetch_related('ambito').all()
    serializer_class = GroupWithAmbitoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    app_name = 'Perfiles'

    def get_permissions(self):
        """niveles/ es público; el resto requiere autenticación."""
        from rest_framework.permissions import AllowAny
        if self.action == 'niveles':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='niveles')
    def niveles(self, request):
        """Retorna los niveles de ámbito disponibles para poblar selectors en el frontend."""
        return Response([
            {'valor': nivel, 'etiqueta': etiqueta}
            for nivel, etiqueta in NIVEL_CHOICES
        ])

    @action(detail=True, methods=['get', 'put', 'patch'], url_path='ambito')
    def ambito(self, request, pk=None):
        """
        GET  → retorna el ámbito del perfil.
        PUT/PATCH → actualiza el ámbito del perfil.
        """
        group = self.get_object()

        if request.method == 'GET':
            try:
                serializer = PerfilAmbitoSerializer(group.ambito)
                return Response(serializer.data)
            except PerfilAmbito.DoesNotExist:
                return Response({'nivel': 4, 'zona': None, 'distrito': None, 'grupo': None})

        # PUT / PATCH
        try:
            instance = group.ambito
        except PerfilAmbito.DoesNotExist:
            instance = PerfilAmbito(group=group)

        serializer = PerfilAmbitoSerializer(
            instance,
            data=request.data,
            partial=(request.method == 'PATCH')
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(group=group)
        return Response(serializer.data)
