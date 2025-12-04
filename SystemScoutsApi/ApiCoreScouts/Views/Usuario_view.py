# ApiCoreScouts/Views/Usuario_view.py
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from ..Serializers import Usuario_serializer as MU_S
from ..Models.usuario_model import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Permissions import PerfilPermission
from rest_framework_simplejwt.views import TokenObtainPairView
from ..Serializers.Usuario_serializer import MyTokenObtainPairSerializer
from ..Filters.usuario_filter import PerfilAplicacionFilter, UsuarioFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('usu_id')
    serializer_class = MU_S.UsuarioSerializer
    # Bypass temporal completo: sin auth ni perfil
    authentication_classes = []
    permission_classes = [AllowAny]
    
    # Optimización: Paginación y Filtros
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UsuarioFilter
    search_fields = ['usu_username', 'usu_email']
    ordering_fields = ['usu_id', 'usu_username', 'usu_email']

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

    @action(detail=False, methods=['post'], url_path='bulk-update-status')
    def bulk_update_status(self, request):
        ids = request.data.get('ids', [])
        vigente = request.data.get('vigente')
        
        if not isinstance(ids, list) or vigente is None:
            return Response(
                {'error': 'Se requiere una lista de IDs y el estado vigente (bool)'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                updated_count = Usuario.objects.filter(usu_id__in=ids).update(usu_vigente=vigente)
                return Response({'status': 'success', 'updated': updated_count})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = MU_S.PerfilSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'], url_path='update-permissions')
    def update_permissions(self, request, pk=None):
        perfil = self.get_object()
        permisos_data = request.data.get('permisos', [])
        
        if not isinstance(permisos_data, list):
            return Response(
                {'error': 'El formato de permisos debe ser una lista'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Opcional: Eliminar permisos existentes si se quiere un reemplazo total
                # Perfil_Aplicacion.objects.filter(pel_id=perfil).delete()
                
                updated_permissions = []
                for p_data in permisos_data:
                    apl_id = p_data.get('apl_id') or p_data.get('APL_ID')
                    if not apl_id:
                        continue
                        
                    # Buscar o crear el permiso
                    permiso, created = Perfil_Aplicacion.objects.get_or_create(
                        pel_id=perfil,
                        apl_id_id=apl_id,
                        defaults={
                            'pea_consultar': False,
                            'pea_ingresar': False,
                            'pea_modificar': False,
                            'pea_eliminar': False
                        }
                    )
                    
                    # Actualizar campos
                    permiso.pea_consultar = p_data.get('pea_consultar', permiso.pea_consultar)
                    permiso.pea_ingresar = p_data.get('pea_ingresar', permiso.pea_ingresar)
                    permiso.pea_modificar = p_data.get('pea_modificar', permiso.pea_modificar)
                    permiso.pea_eliminar = p_data.get('pea_eliminar', permiso.pea_eliminar)
                    permiso.save()
                    
                    updated_permissions.append(permiso)
                
                return Response({'status': 'success', 'updated': len(updated_permissions)})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    filterset_class = PerfilAplicacionFilter


