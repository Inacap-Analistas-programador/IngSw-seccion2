# ApiCoreScouts/Views/Usuario_view.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
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
    # Bypass temporal completo: sin auth ni perfil
    authentication_classes = []
    permission_classes = [AllowAny]

    # Envoltorio para capturar y loggear excepciones durante list (500s)
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            # Imprimir traceback en la salida del servidor para debugging
            print('--- Exception in UsuarioViewSet.list ---')
            print(tb)
            from rest_framework.response import Response
            from rest_framework import status
            return Response({'detail': 'internal_server_error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = MU_S.PerfilSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

class AplicacionViewSet(viewsets.ModelViewSet):
    queryset = Aplicacion.objects.all()
    serializer_class = MU_S.AplicacionSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

class PerfilAplicacionViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Aplicacion.objects.all()
    serializer_class = MU_S.PerfilAplicacionSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


