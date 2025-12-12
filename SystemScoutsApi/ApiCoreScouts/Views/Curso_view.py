from ..Models.curso_model import *
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Serializers import Curso_serializer as MC_S
from ..Filters import curso_filter as CF
from ..Permissions import PerfilPermission
from django.db.models import Prefetch

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CursoViewSet(viewsets.ModelViewSet):
    serializer_class = MC_S.CursoSerializer
    filterset_class = CF.CursoFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = "Cursos"
    ACTION_PERMISSIONS = {
        'list': ('pea_consultar',),
        'retrieve': ('pea_consultar',),
        'create': ('pea_ingresar',),
        'update': ('pea_modificar',),
        'partial_update': ('pea_modificar',),
        'destroy': ('pea_eliminar',),
    }
    
    def get_queryset(self):
        """Optimizar queries con select_related y prefetch_related"""
        return Curso.objects.select_related(
            'usu_id',               # Usuario
            'tcu_id',               # Tipo_Curso
            'per_id_responsable',   # Persona responsable
            'car_id_responsable',   # Cargo responsable
            'com_id_lugar'          # Comuna lugar
        ).order_by('cur_estado', 'cur_descripcion')
        # .prefetch_related(
        #     # Prefetch secciones del curso
        #     Prefetch(
        #         'curso_seccion',
        #         Curso_Seccion.objects.select_related('ram_id')
        #     ),
        #     # Prefetch coordinadores del curso
        #     Prefetch(
        #         'curso_coordinador',
        #         Curso_Coordinador.objects.select_related('per_id', 'car_id')
        #     ),
        #     # Prefetch formadores del curso
        #     Prefetch(
        #         'curso_formador',
        #         Curso_Formador.objects.select_related('per_id', 'rol_id', 'cus_id__cur_id')
        #     )
        # ).order_by('cur_estado', 'cur_descripcion')

class CursoCuotaViewSet(viewsets.ModelViewSet):
    serializer_class = MC_S.CursoCuotaSerializer
    filterset_class = CF.CursoCuotaFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Curso_Cuota.objects.select_related(
            'cur_id'  # Curso
        ).order_by('cuu_fecha', 'cuu_id')

class CursoFechaViewSet(viewsets.ModelViewSet):
    serializer_class = MC_S.CursoFechaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Curso_Fecha.objects.select_related(
            'cur_id'  # Curso
        ).all()

class CursoAlimentacionViewSet(viewsets.ModelViewSet):
    serializer_class = MC_S.CursoAlimentacionSerializer
    filterset_class = CF.CursoAlimentacionFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Curso_Alimentacion.objects.select_related(
            'cua_id'  # Curso_Seccion
        ).order_by('cua_fecha', 'cua_tiempo', 'cua_id')

class CursoCoordinadorViewSet(viewsets.ModelViewSet):
    serializer_class = MC_S.CursoCoordinadorSerializer
    filterset_class = CF.CursoCoordinadorFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Curso_Coordinador.objects.select_related(
            'cur_id',   # Curso
            'per_id',   # Persona
            'car_id'    # Cargo
        ).order_by('cuc_id')

class CursoSeccionViewSet(viewsets.ModelViewSet):
    serializer_class = MC_S.CursoSeccionSerializer
    filterset_class = CF.CursoSeccionFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Curso_Seccion.objects.select_related(
            'cur_id',   # Curso
            'ram_id'    # Rama
        ).prefetch_related(
            Prefetch(
                'persona_curso',
                Persona_Curso.objects.select_related('per_id', 'rol_id', 'ali_id', 'niv_id')
            )
        ).order_by('cus_seccion', 'cus_id')

class CursoFormadorViewSet(viewsets.ModelViewSet):
    serializer_class = MC_S.CursoFormadorSerializer
    filterset_class = CF.CursoFormadorFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Curso_Formador.objects.select_related(
            'cur_id',   # Curso
            'per_id',   # Persona
            'rol_id',   # Rol
            'cus_id__cur_id'  # Curso_Seccion -> Curso
        ).order_by('cuf_id')
