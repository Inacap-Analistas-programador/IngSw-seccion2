from rest_framework import viewsets
from ..Serializers import Usuarios_serializers as MU_S
from ..Models.ModuloUsuarios import *

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = MU_S.UsuarioSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = MU_S.PerfilSerializer

class AplicacionViewSet(viewsets.ModelViewSet):
    queryset = Aplicacion.objects.all()
    serializer_class = MU_S.AplicacionSerializer

class PerfilAplicacionViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Aplicacion.objects.all()
    serializer_class = MU_S.PerfilAplicacionSerializer


