# ApiCoreScouts/Views/Usuario_view.py
from rest_framework import viewsets
from ..Serializers import Usuario_serializer as MU_S
from ..Models.usuario_model import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Permissions import PerfilPermission
from rest_framework_simplejwt.views import TokenObtainPairView
from ..Serializers.Usuario_serializer import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = MU_S.UsuarioSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = MU_S.PerfilSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Perfiles"

class AplicacionViewSet(viewsets.ModelViewSet):
    queryset = Aplicacion.objects.all()
    serializer_class = MU_S.AplicacionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Aplicaciones"

class PerfilAplicacionViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Aplicacion.objects.all()
    serializer_class = MU_S.PerfilAplicacionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "PerfilAplicacion"


