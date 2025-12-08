from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Serializers import Persona_serializer as MU_S
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from ..Filters.persona_filter import *
from ..Models.persona_model import *
from ..Permissions import PerfilPermission

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = MU_S.PersonaCompletaSerializer  # Usar el serializer con datos relacionados
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonaFilter
    renderer_classes = [JSONRenderer]
    
    @action(detail=True, methods=['get'], url_path='cursos')
    def cursos(self, request, pk=None):
        """Obtener todos los cursos de una persona"""
        try:
            persona = self.get_object()
            cursos_persona = Persona_Curso.objects.filter(per_id=persona.per_id)
            serializer = MU_S.PersonaCursoSerializer(cursos_persona, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class PersonaCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Curso.objects.all()
    serializer_class = MU_S.PersonaCursoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonaCursoFilter
    renderer_classes = [JSONRenderer]

class PersonaGrupoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Grupo.objects.all()
    serializer_class = MU_S.PersonaGrupoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

class PersonaFormadorViewSet(viewsets.ModelViewSet):
    queryset = Persona_Formador.objects.all()
    serializer_class = MU_S.PersonaFormadorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

class PersonaIndividualViewSet(viewsets.ModelViewSet):
    queryset = Persona_Individual.objects.all()
    serializer_class = MU_S.PersonaIndividualSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

class PersonaNivelViewSet(viewsets.ModelViewSet):
    queryset = Persona_Nivel.objects.all()
    serializer_class = MU_S.PersonaNivelSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

class PersonaEstadoCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Estado_Curso.objects.all()
    serializer_class = MU_S.PersonaEstadoCursoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

class PersonaVehiculoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Vehiculo.objects.all()
    serializer_class = MU_S.PersonaVehiculoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'
