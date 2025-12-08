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
from django.db.models import Prefetch

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PersonaViewSet(viewsets.ModelViewSet):
    serializer_class = MU_S.PersonaCompletaSerializer  # Usar el serializer con datos relacionados
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonaFilter
    renderer_classes = [JSONRenderer]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """
        Optimizar queries con select_related y prefetch_related
        para evitar N+1 query problems
        """
        queryset = Persona.objects.select_related(
            'esc_id',           # Estado_Civil
            'com_id',           # Comuna
            'usu_id'            # Usuario
        ).prefetch_related(
            # Prefetch Persona_Curso con sus relaciones
            Prefetch(
                'persona_curso',
                Persona_Curso.objects.select_related(
                    'cus_id__cur_id',   # Curso_Seccion -> Curso
                    'rol_id',            # Rol
                    'ali_id',            # Alimentacion
                    'niv_id'             # Nivel
                ).prefetch_related(
                    Prefetch(
                        'persona_curso_estado',  # Persona_Estado_Curso
                        Persona_Estado_Curso.objects.select_related('usu_id')
                    )
                )
            ),
            # Prefetch otras relaciones
            Prefetch('persona_grupo__gru_id'),
            Prefetch('persona_formador'),
            Prefetch('persona_individual__car_id'),
            Prefetch('persona_nivel__niv_id'),
            Prefetch('persona_vehiculo')
        ).all()
        
        return queryset
    
    @action(detail=True, methods=['get'], url_path='cursos')
    def cursos(self, request, pk=None):
        """Obtener todos los cursos de una persona con relaciones optimizadas"""
        try:
            persona = self.get_object()
            # Usar las relaciones ya precargadas
            cursos_persona = persona.persona_curso.all()
            serializer = MU_S.PersonaCursoSerializer(cursos_persona, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class PersonaCursoViewSet(viewsets.ModelViewSet):
    serializer_class = MU_S.PersonaCursoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonaCursoFilter
    renderer_classes = [JSONRenderer]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """
        Optimizar queries con select_related para relaciones FK
        """
        return Persona_Curso.objects.select_related(
            'per_id',               # Persona
            'cus_id__cur_id',       # Curso_Seccion -> Curso
            'rol_id',               # Rol
            'ali_id',               # Alimentacion
            'niv_id'                # Nivel
        ).prefetch_related(
            # Prefetch Estado del curso si existe relación inversa
            Prefetch(
                'persona_estado_curso',  # Ajustar según nombre de relación inversa
                Persona_Estado_Curso.objects.select_related('usu_id')
            )
        ).all()

class PersonaGrupoViewSet(viewsets.ModelViewSet):
    serializer_class = MU_S.PersonaGrupoSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Persona_Grupo.objects.select_related(
            'per_id',    # Persona
            'gru_id'     # Grupo
        ).all()

class PersonaFormadorViewSet(viewsets.ModelViewSet):
    serializer_class = MU_S.PersonaFormadorSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Persona_Formador.objects.select_related(
            'per_id'     # Persona
        ).all()

class PersonaIndividualViewSet(viewsets.ModelViewSet):
    serializer_class = MU_S.PersonaIndividualSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Persona_Individual.objects.select_related(
            'per_id',    # Persona
            'car_id',    # Cargo
            'dis_id',    # Distrito
            'zon_id'     # Zona
        ).all()

class PersonaNivelViewSet(viewsets.ModelViewSet):
    serializer_class = MU_S.PersonaNivelSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Persona_Nivel.objects.select_related(
            'per_id',    # Persona
            'niv_id',    # Nivel
            'ram_id'     # Rama
        ).all()

class PersonaEstadoCursoViewSet(viewsets.ModelViewSet):
    serializer_class = MU_S.PersonaEstadoCursoSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Persona_Estado_Curso.objects.select_related(
            'usu_id',    # Usuario
            'pec_id__per_id',     # Persona_Curso -> Persona
            'pec_id__cus_id__cur_id'  # Persona_Curso -> Curso_Seccion -> Curso
        ).all()

class PersonaVehiculoViewSet(viewsets.ModelViewSet):
    serializer_class = MU_S.PersonaVehiculoSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Persona_Vehiculo.objects.select_related(
            'pec_id__per_id',      # Persona_Curso -> Persona
            'pec_id__cus_id__cur_id'  # Persona_Curso -> Curso_Seccion -> Curso
        ).all()
