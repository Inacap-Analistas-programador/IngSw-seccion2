from ..Models.curso_model import *
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Serializers import Curso_serializer as MC_S
from ..Filters import curso_filter as CF
from ..Permissions import PerfilPermission
from rest_framework.permissions import AllowAny
from django.db.models import Prefetch, Q
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CursoViewSet(viewsets.ModelViewSet):
    serializer_class = MC_S.CursoSerializer
    filterset_class = CF.CursoFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = []
    permission_classes = [AllowAny]
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
        ).prefetch_related(
            # Prefetch secciones del curso
            Prefetch(
                'curso_seccion_set',
                Curso_Seccion.objects.select_related('ram_id')
            ),
            # Prefetch coordinadores del curso
            Prefetch(
                'curso_coordinador_set',
                Curso_Coordinador.objects.select_related('per_id', 'car_id')
            ),
            # Prefetch formadores del curso
            Prefetch(
                'curso_formador_set',
                Curso_Formador.objects.select_related('per_id', 'rol_id', 'cus_id__cur_id')
            ),
            'curso_fecha_set',
            'curso_cuota_set',
            'curso_alimentacion_set',
        ).order_by('cur_estado', 'cur_descripcion')

    @action(detail=False, methods=['get'])
    def para_mantenedor(self, request):
        """
        Endpoint ultra-optimizado para la tabla principal del mantenedor de Cursos.
        Retorna solo los campos mínimos para la tabla.
        """
        queryset = Curso.objects.prefetch_related(
            'curso_fecha_set'
        )
        queryset = self.filter_queryset(queryset).distinct().order_by('-cur_id')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MC_S.CursoMantenedorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MC_S.CursoMantenedorSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_cursos_acreditacion(self, request):
        """
        Retorna cursos vigentes que inician hoy o mañana.
        """
        # Calcular fechas en la zona horaria del servidor (o configurada)
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        
        cursos = Curso.objects.filter(
            cur_estado=1,
            curso_fecha__cuf_fecha_inicio__date__in=[today, tomorrow]
        ).distinct().order_by('cur_descripcion')
        
        data = []
        for c in cursos:
            data.append({
                'cur_id': c.cur_id,
                'cur_descripcion': c.cur_descripcion
            })
            
        return Response(data)

    @action(detail=True, methods=['get'])
    def get_alimentacion_curso(self, request, pk=None):
        """
        Retorna opciones de alimentación para un curso específico,
        optimizadas para el formulario de registro.
        """
        curso = self.get_object()
        alimentaciones = Curso_Alimentacion.objects.filter(
            cur_id=curso,
            cua_vigente=True
        ).select_related('ali_id')

        # Mapeo de cua_tiempo a nombres legibles
        tiempos = {
            1: 'Desayuno',
            2: 'Almuerzo',
            3: 'Once',
            4: 'Cena',
            5: 'Once/Cena',
        }

        data = []
        for a in alimentaciones:
            tiempo_str = tiempos.get(a.cua_tiempo, 'Otro')
            data.append({
                'cua_id': a.cua_id,
                'ali_id': a.ali_id.ali_id,
                'label': f"[{tiempo_str}] {a.cua_descripcion}"
            })

        return Response(data)

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
    filterset_class = CF.CursoFechaFilter
    pagination_class = StandardResultsSetPagination
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
            'cur_id',  # Curso
            'ali_id'   # Alimentacion
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
    authentication_classes = []
    permission_classes = [AllowAny]
    app_name = "Cursos"
    ACTION_PERMISSIONS = CursoViewSet.ACTION_PERMISSIONS
    
    def get_queryset(self):
        """Optimizar queries con select_related"""
        return Curso_Seccion.objects.select_related(
            'cur_id',   # Curso
            'ram_id'    # Rama
        ).prefetch_related(
            Prefetch(
                'persona_curso_set',
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
