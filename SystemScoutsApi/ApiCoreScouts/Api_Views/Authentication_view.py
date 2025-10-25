# ApiCoreScouts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from ..Serializers.Usuarios_serializers import CustomTokenObtainPairSerializer

# Vista personalizada para login
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Vista protegida de ejemplo
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    """Obtener perfil del usuario autenticado"""
    usuario = request.user
    return Response({
        'USU_ID': usuario.USU_ID,
        'USU_USERNAME': usuario.USU_USERNAME,
        'PEL_ID': usuario.PEL_ID.PEL_ID,
        'PEL_DESCRIPCION': usuario.PEL_ID.PEL_DESCRIPCION,
        'USU_RUTA_FOTO': usuario.USU_RUTA_FOTO,
        'USU_VIGENTE': usuario.USU_VIGENTE,
    })

# Vista pública de ejemplo
@api_view(['GET'])
@permission_classes([AllowAny])
def saludar(request):
    return Response({'message': '¡Bienvenido a System Scouts API!'})

# Vista protegida con estructura api/<recurso>/<subrecurso>
class RecursoPrincipalView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, recurso_secundario=None):
        if recurso_secundario:
            return Response({
                'message': f'Accediendo a recurso secundario: {recurso_secundario}',
                'usuario': request.user.USU_USERNAME,
                'metodo': 'GET'
            })
        else:
            return Response({
                'message': 'Listando recursos principales',
                'usuario': request.user.USU_USERNAME,
                'metodo': 'GET'
            })
    
    def post(self, request, recurso_secundario=None):
        return Response({
            'message': f'Creando en recurso: {recurso_secundario}' if recurso_secundario else 'Creando recurso principal',
            'usuario': request.user.USU_USERNAME,
            'data': request.data,
            'metodo': 'POST'
        })