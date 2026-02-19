from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..Serializers import Persona_serializer as MU_S
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from ..Filters.persona_filter import *
from ..Models.persona_model import *
from ..Models.pago_model import Pago_Persona
from ..Permissions import PerfilPermission
from django.db.models import Prefetch, Q, Value, CharField
from django.db.models.functions import Concat

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PersonaViewSet(viewsets.ModelViewSet):
    serializer_class = MU_S.PersonaCompletaSerializer  # Usar el serializer con datos relacionados
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Personas'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PersonaFilter
    search_fields = ['per_nombres', 'per_apelpta', 'per_apelmat', 'per_run', 'per_apodo']
    renderer_classes = [JSONRenderer]
    pagination_class = StandardResultsSetPagination

    @action(detail=False, methods=['post'])
    def acreditacion_manual_acreditar(self, request):
        """
        Acción para acreditar un participante manualmente.
        Recibe { 'per_id': <int>, 'rut': <str> }
        """
        try:
            data = request.data
            per_id = data.get('per_id')
            
            # import models inside if not available or rely on global imports
            # (Imports are available globally in this file)
            
            # Buscar persona
            persona = Persona.objects.filter(per_id=per_id).first()
            if not persona:
                return Response({'error': 'Persona no encontrada'}, status=404)

            # Buscar curso activo (Persona_Curso)
            pec = Persona_Curso.objects.filter(per_id=per_id).first()
            if not pec:
                return Response({'error': 'La persona no está inscrita en ningún curso'}, status=400)

            # Realizar acreditación
            pec.pec_acreditacion = True
            pec.pec_registro = True
            pec.save()

            # Retornar datos actualizados usando el serializer completo
            serializer = self.get_serializer(persona)
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['get'])
    def para_correos(self, request):
        """
        Endpoint optimizado que retorna solo lo mínimo para la vista de Correos.
        Requiere filtrar por curso para evitar ambigüedad en Persona_Curso.
        """
        curso_desc = request.query_params.get('curso_descripcion')
        curso_id = request.query_params.get('curso_id')
        
        # Base queryset para Persona_Curso
        pc_qs = Persona_Curso.objects.select_related('cus_id__cur_id', 'rol_id').only(
            'pec_id', 'per_id', 'cus_id', 'rol_id', 'pec_envio_correo_qr'
        ).order_by('-pec_envio_correo_qr', '-pec_id')
        
        # Prefetch de Persona_Curso optimizado
        # Note: related_name is 'persona_curso_set' (default), but related_query_name is 'persona_curso' (model name)
        queryset = Persona.objects.prefetch_related(
            Prefetch('persona_curso_set', queryset=pc_qs)
        )

        # Standard filtering (uses PersonaFilter which uses 'persona_curso')
        queryset = self.filter_queryset(queryset).distinct().order_by('per_id')
        
        # Si se pide todo o un page_size grande, desactivar paginación localmente
        page_size = request.query_params.get('page_size')
        if page_size and int(page_size) >= 1000:
            pagination = self.paginate_queryset(queryset)
            if pagination is not None:
                serializer = MU_S.PersonaCorreoSerializer(pagination, many=True)
                return self.get_paginated_response(serializer.data)
        
        serializer = MU_S.PersonaCorreoSerializer(queryset, many=True)
        return Response(serializer.data)
    
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
                'persona_curso_set',
                queryset=Persona_Curso.objects.select_related(
                    'cus_id__cur_id',   # Curso_Seccion -> Curso
                    'rol_id',            # Rol
                    'ali_id',            # Alimentacion
                    'niv_id'             # Nivel
                ).prefetch_related(
                    Prefetch(
                        'persona_estado_curso_set',  # Persona_Estado_Curso
                        queryset=Persona_Estado_Curso.objects.select_related('usu_id')
                    )
                )
            ),
            # Prefetch otras relaciones
            Prefetch('persona_grupo_set', queryset=Persona_Grupo.objects.select_related('gru_id')),
            Prefetch('persona_formador_set'),
            Prefetch('persona_individual_set', queryset=Persona_Individual.objects.select_related('car_id')),
            Prefetch('persona_nivel_set', queryset=Persona_Nivel.objects.select_related('niv_id')),
        ).all()
        return queryset
    
    @action(detail=True, methods=['get'], url_path='cursos')
    def cursos(self, request, pk=None):
        """Obtener todos los cursos de una persona con relaciones optimizadas"""
        try:
            persona = self.get_object()
            # Usar las relaciones ya precargadas
            cursos_persona = persona.persona_curso_set.all()
            serializer = MU_S.PersonaCursoSerializer(cursos_persona, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['post'], url_path='acreditacion_manual_acreditar')
    def acreditacion_manual_acreditar(self, request):
        """
        Acción personalizada para acreditar a una persona manualmente.
        Recibe 'per_id' y 'rut' en el body.
        """
        try:
            per_id = request.data.get('per_id')
            rut = request.data.get('rut') # Opcional, para validación extra

            if not per_id:
                return Response({'error': 'per_id es requerido'}, status=400)

            # Buscar la Persona
            try:
                persona = Persona.objects.get(pk=per_id)
            except Persona.DoesNotExist:
                return Response({'error': 'Persona no encontrada'}, status=404)

            # Buscar la inscripción (Persona_Curso) vigente para acreditar
            # Asumimos que se acredita en el curso activo/vigente (Estado 1 = Vigente).
            inscripciones = Persona_Curso.objects.filter(
                per_id=persona,
                cus_id__cur_id__cur_estado=1
            )
            
            # Si no hay cursos vigentes, fallback a la última inscripción
            if not inscripciones.exists():
                 inscripciones = Persona_Curso.objects.filter(per_id=persona).order_by('-pec_id')

            if not inscripciones.exists():
                return Response({'error': 'No se encontró inscripción para acreditar'}, status=404)

            # Acreditar la primera encontrada (o la más reciente)
            inscripcion = inscripciones.first()
            inscripcion.pec_acreditacion = True
            inscripcion.save()

            # Retornar datos actualizados (puedes usar el serializer si quieres)
            return Response({
                'per_id': persona.per_id,
                'nombre': f"{persona.per_nombres} {persona.per_apelpta}",
                'acreditado': True,
                'mensaje': 'Acreditación exitosa'
            })

        except Exception as e:
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['get'])
    def search_acreditacion(self, request):
        """
        Endpoint optimizado para búsqueda en Acreditación Manual.
        Retorna solo los datos necesarios para la UI de acreditación.
        """
        term = request.query_params.get('search', '').strip()
        curso_id = request.query_params.get('curso_id')

        if not term and not curso_id:
            return Response([])

        queryset = Persona.objects.all()

        # 1. Filtro por término (Nombre o RUT)
        if term:
            # Anotamos el RUT completo para buscar por "12345678-9"
            queryset = queryset.annotate(
                full_rut=Concat('per_run', Value('-'), 'per_dv', output_field=CharField())
            )
            
            # Separar términos para permitir búsqueda flexible (ej: "Juan Perez" o "Juan Gonzalez")
            terms = term.split()
            for t in terms:
                queryset = queryset.filter(
                    Q(per_nombres__icontains=t) |
                    Q(per_apelpta__icontains=t) |
                    Q(per_apelmat__icontains=t) |
                    Q(per_run__icontains=t) |
                    Q(full_rut__icontains=t) |  # Búsqueda por RUT completo (con guión)
                    Q(per_apodo__icontains=t)
                )

        # 2. Filtro por curso específico (opcional)
        if curso_id:
            queryset = queryset.filter(
                persona_curso__cus_id__cur_id=curso_id
            )

        # 3. Optimización de consultas (Prefetch)
        # Nota: Persona_Vehiculo se relaciona con Persona_Curso (pec_id), no con Persona directamente.
        queryset = queryset.select_related('esc_id', 'com_id').prefetch_related(
            Prefetch(
                'persona_curso_set',
                queryset=Persona_Curso.objects.select_related('cus_id__cur_id', 'ali_id', 'rol_id')
                                             .prefetch_related('persona_vehiculo_set') # Vehículos de esa inscripción
                                             .order_by('-pec_id')
            ),
             # Optimizar pagos: traer solo los confirmados (1)
            Prefetch(
                'pago_persona_set',
                queryset=Pago_Persona.objects.filter(pap_estado=1)
            )
        ).distinct().order_by('per_nombres', 'per_apelpta')[:20] # Limitar a 20 resultados para rapidez

        data = []
        for p in queryset:
            # Lógica para determinar curso y estado
            # Prioridad: Curso seleccionado (si hay filtro), o último curso inscrito
            pc_list = list(p.persona_curso_set.all())
            current_pc = None
            
            if curso_id:
                # Buscar el específico
                current_pc = next((pc for pc in pc_list if str(pc.cus_id.cur_id.cur_id) == str(curso_id)), None)
            
            if not current_pc and pc_list:
                # Si no se filtrar por curso o no se encontró, usar el más reciente
                current_pc = pc_list[0]

            # Datos derivados
            curso_nombre = current_pc.cus_id.cur_id.cur_descripcion if (current_pc and current_pc.cus_id and current_pc.cus_id.cur_id) else "Sin Curso"
            rama_nombre = "" # Se podría sacar de Nivel si es crítico, por ahora vacío o simple
            
            # Pago confirmado
            pago_list = list(p.pago_persona_set.all())
            pago_confirmado = len(pago_list) > 0

            # Acreditado (en el curso actual)
            acreditado = current_pc.pec_acreditacion if current_pc else False
            
            # Vehículo: Revisar si tiene vehículo en la inscripción actual
            # Ojo: la relación es Persona_Curso -> Persona_Vehiculo
            tiene_vehiculo = False
            if current_pc:
                # persona_vehiculo_set es el related_name por defecto de fk en Persona_Vehiculo hacia Persona_Curso
                tiene_vehiculo = current_pc.persona_vehiculo_set.exists()

            # Alimentación
            diet = current_pc.ali_id.ali_descripcion if (current_pc and current_pc.ali_id) else "Normal"
            
            # Construir objeto ligero
            data.append({
                'per_id': p.per_id,
                'name': f"{p.per_nombres} {p.per_apelpta}",
                'nickname': p.per_apodo or "",
                'rut': f"{p.per_run}-{p.per_dv}" if p.per_run else "",
                'currentCourse': curso_nombre,
                'branchName': rama_nombre,
                'vehicle': tiene_vehiculo,
                'dietType': diet,
                'paymentConfirmed': pago_confirmado,
                'paymentStatus': 'Confirmado' if pago_confirmado else 'Pendiente',
                'acreditationStatus': 'Acreditado' if acreditado else 'Pendiente',
                'per_curso_id': current_pc.cus_id.cur_id.cur_id if (current_pc and current_pc.cus_id and current_pc.cus_id.cur_id) else None
            })

        return Response(data)

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
        ).all()
        # .prefetch_related(
        #     # Prefetch Estado del curso si existe relación inversa
        #     Prefetch(
        #         'persona_estado_curso',  # Ajustar según nombre de relación inversa
        #         Persona_Estado_Curso.objects.select_related('usu_id')
        #     )
        # ).all()

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

