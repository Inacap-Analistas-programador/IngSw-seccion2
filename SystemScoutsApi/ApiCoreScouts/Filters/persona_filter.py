import django_filters
from django.db.models import Q
from ..Models.persona_model import *
from datetime import datetime, timedelta

class PersonaFilter(django_filters.FilterSet):
    # --- Filtros de identidad ---
    nombre = django_filters.CharFilter(field_name='per_nombres',lookup_expr='icontains',
        label='Filtrar por nombre')
    apellido = django_filters.CharFilter(field_name='per_apelpta',lookup_expr='icontains',
        label='Filtrar por apellido')
    run = django_filters.CharFilter(field_name='per_run',lookup_expr='exact',
        label='Filtrar por RUN')
    dv = django_filters.CharFilter(field_name='per_dv',lookup_expr='iexact',
        label='Filtrar por dígito verificador')
    
    # --- Filtros de contacto ---
    email = django_filters.CharFilter(field_name='per_mail',lookup_expr='icontains',
        label='Filtrar por email')
    telefono = django_filters.CharFilter(field_name='per_fono',lookup_expr='icontains',
        label='Filtrar por teléfono')
    
    # --- Filtros de ubicación ---
    comuna_nombre = django_filters.CharFilter(field_name='com_id__com_descripcion',lookup_expr='icontains',
        label='Filtrar por nombre de comuna')
    comuna_id = django_filters.NumberFilter(field_name='com_id__com_id',
        label='Filtrar por ID de comuna')
    
    # --- Filtro de edad (rango) ---
    edad_minima = django_filters.NumberFilter(
        method='filter_edad_minima',
        label='Edad mínima')
    edad_maxima = django_filters.NumberFilter(
        method='filter_edad_maxima',
        label='Edad máxima')
    
    # --- Filtro de género/sexo (basado en Estado Civil o apellido materno) ---
    genero = django_filters.ChoiceFilter(
        method='filter_genero',
        choices=[
            ('M', 'Masculino'),
            ('F', 'Femenino'),
            ('O', 'Otro'),
        ],
        label='Filtrar por género')
    
    # --- Filtro de fecha de inscripción (rango) ---
    fecha_inscripcion_desde = django_filters.DateTimeFilter(
        field_name='per_fecha_hora',
        lookup_expr='gte',
        label='Fecha de inscripción desde')
    fecha_inscripcion_hasta = django_filters.DateTimeFilter(
        field_name='per_fecha_hora',
        lookup_expr='lte',
        label='Fecha de inscripción hasta')
    
    # --- Filtro de estado de acreditación (a través de Persona_Curso) ---
    acreditado = django_filters.BooleanFilter(
        field_name='persona_curso__pec_acreditacion',
        label='Filtrar por estado de acreditación')
    
    correo_qr_enviado = django_filters.BooleanFilter(
        field_name='persona_curso__pec_envio_correo_qr',
        label='Filtrar por correo enviado')
    
    # --- Filtro de cursos asociados ---
    curso_codigo = django_filters.CharFilter(
        field_name='persona_curso__cus_id__cur_id__cur_codigo',
        lookup_expr='iexact',
        label='Filtrar por código de curso')
    
    curso_descripcion = django_filters.CharFilter(
        field_name='persona_curso__cus_id__cur_id__cur_descripcion',
        lookup_expr='icontains',
        label='Filtrar por descripción de curso')
    
    # --- Filtros de Roles y Ramas (a través de Persona_Curso) ---
    rol_id = django_filters.NumberFilter(
        field_name='persona_curso__rol_id',
        label='Filtrar por ID de rol'
    )
    ram_id = django_filters.NumberFilter(
        field_name='persona_curso__niv_id__ram_id',
        label='Filtrar por ID de rama'
    )
    # -----------------------------------------------------------
    
    # --- Filtros de usuario y vigencia ---
    usuario_nombre = django_filters.CharFilter(field_name='usu_id__usu_username',lookup_expr='icontains',
        label='Filtrar por nombre de usuario')
    usuario_id = django_filters.NumberFilter(field_name='usu_id__usu_id',
        label='Filtrar por ID de usuario')
    vigente = django_filters.BooleanFilter(field_name='per_vigente',
        label='Filtrar por vigencia')

    class Meta:
        model = Persona
        fields = ['nombre',
                  'apellido',
                  'run',
                  'dv',
                  'email',
                  'telefono',
                  'comuna_nombre',
                  'comuna_id',
                  'edad_minima',
                  'edad_maxima',
                  'genero',
                  'fecha_inscripcion_desde',
                  'fecha_inscripcion_hasta',
                  'acreditado',
                  'curso_codigo',
                  'curso_descripcion',
                  'rol_id',
                  'ram_id',
                  'usuario_nombre',
                  'usuario_id',
                  'vigente'
                  ]
    
    def filter_edad_minima(self, queryset, name, value):
        """Filtrar personas con edad mínima"""
        if value:
            fecha_limite = datetime.now() - timedelta(days=value*365)
            return queryset.filter(per_fecha_nac__lte=fecha_limite)
        return queryset
    
    def filter_edad_maxima(self, queryset, name, value):
        """Filtrar personas con edad máxima"""
        if value:
            fecha_limite = datetime.now() - timedelta(days=value*365)
            return queryset.filter(per_fecha_nac__gte=fecha_limite)
        return queryset
    
    def filter_genero(self, queryset, name, value):
        """
        Filtrar por género/sexo basado en estado civil:
        M = Masculino, F = Femenino, O = Otro
        Nota: Ajustar según tu lógica de negocio
        """
        if value == 'M':
            # Personas con estado civil "Soltero", "Casado", "Divorciado" (típicamente masculinos)
            return queryset.filter(esc_id__esc_descripcion__in=['Soltero', 'Casado', 'Divorciado'])
        elif value == 'F':
            # Personas con apellido materno (típicamente femeninos)
            return queryset.filter(per_apelmat__isnull=False)
        return queryset


class PersonaCursoFilter(django_filters.FilterSet):
    """
    Filtros para Persona_Curso, con soporte para búsqueda profunda
    en Persona, Curso_Seccion, Curso, Rol, Alimentación y Nivel.
    """

    # --- Filtros sobre Persona ---
    run = django_filters.CharFilter(
        field_name='per_id__per_run',
        lookup_expr='iexact',
        label='Filtrar por RUN (sin DV)'
    )
    dv = django_filters.CharFilter(
        field_name='per_id__per_dv',
        lookup_expr='iexact',
        label='Filtrar por dígito verificador'
    )
    nombre_persona = django_filters.CharFilter(
        field_name='per_id__per_nombres',
        lookup_expr='icontains',
        label='Filtrar por nombre de persona'
    )
    apellido_persona = django_filters.CharFilter(
        field_name='per_id__per_apelpta',
        lookup_expr='icontains',
        label='Filtrar por apellido de persona'
    )

    # --- Filtro sobre Curso ---
    curso_codigo = django_filters.CharFilter(
        field_name='cus_id__cur_id__cur_codigo',
        lookup_expr='iexact',
        label='Filtrar por código de curso (ej: CUR-0778)'
    )

    # --- Filtros sobre relaciones directas ---
    rol_nombre = django_filters.CharFilter(
        field_name='rol_id__rol_descripcion',
        lookup_expr='icontains',
        label='Filtrar por nombre de rol'
    )
    alimentacion_nombre = django_filters.CharFilter(
        field_name='ali_id__ali_descripcion',
        lookup_expr='icontains',
        label='Filtrar por tipo de alimentación'
    )
    nivel_nombre = django_filters.CharFilter(
        field_name='niv_id__niv_descripcion',
        lookup_expr='icontains',
        label='Filtrar por nivel'
    )

    # --- Filtros booleanos ---
    registrado = django_filters.BooleanFilter(
        field_name='pec_registro',
        label='Filtrar por registro completado'
    )
    acreditado = django_filters.BooleanFilter(
        field_name='pec_acreditacion',
        label='Filtrar por acreditación'
    )
    correo_qr_enviado = django_filters.BooleanFilter(
        field_name='pec_envio_correo_qr',
        label='Filtrar por correo QR enviado'
    )

    grupo_id = django_filters.NumberFilter(
        field_name='per_id__persona_grupo__gru_id',
        label='Filtrar por Grupo (Trae cursos de personas en este grupo)'
    )

    class Meta:
        model = Persona_Curso
        fields = [
            'run',
            'dv',
            'nombre_persona',
            'apellido_persona',
            'curso_codigo',
            'rol_nombre',
            'alimentacion_nombre',
            'nivel_nombre',
            'registrado',
            'acreditado',
            'correo_qr_enviado',
            'grupo_id',
        ]


class PersonaGrupoFilter(django_filters.FilterSet):
    """Filtros para Persona_Grupo"""
    persona_run = django_filters.CharFilter(
        field_name='per_id__per_run',
        lookup_expr='iexact',
        label='Filtrar por RUN de persona'
    )
    grupo_id = django_filters.NumberFilter(
        field_name='gru_id__gru_id',
        label='Filtrar por ID de grupo'
    )
    grupo_nombre = django_filters.CharFilter(
        field_name='gru_id__gru_descripcion',
        lookup_expr='icontains',
        label='Filtrar por nombre de grupo'
    )
    vigente = django_filters.BooleanFilter(
        field_name='peg_vigente',
        label='Filtrar por vigencia'
    )

    class Meta:
        model = Persona_Grupo
        fields = ['persona_run', 'grupo_id', 'grupo_nombre', 'vigente']


class PersonaFormadorFilter(django_filters.FilterSet):
    """Filtros para Persona_Formador"""
    persona_run = django_filters.CharFilter(
        field_name='per_id__per_run',
        lookup_expr='iexact',
        label='Filtrar por RUN de persona'
    )
    persona_nombre = django_filters.CharFilter(
        field_name='per_id__per_nombres',
        lookup_expr='icontains',
        label='Filtrar por nombre'
    )
    habilidad_1 = django_filters.BooleanFilter(
        field_name='pef_hab_1',
        label='Tiene habilidad 1'
    )
    habilidad_2 = django_filters.BooleanFilter(
        field_name='pef_hab_2',
        label='Tiene habilidad 2'
    )
    verificado = django_filters.BooleanFilter(
        field_name='pef_verif',
        label='Filtrar por verificación'
    )

    class Meta:
        model = Persona_Formador
        fields = ['persona_run', 'persona_nombre', 'habilidad_1', 'habilidad_2', 'verificado']


class PersonaIndividualFilter(django_filters.FilterSet):
    """Filtros para Persona_Individual"""
    persona_run = django_filters.CharFilter(
        field_name='per_id__per_run',
        lookup_expr='iexact',
        label='Filtrar por RUN'
    )
    cargo_id = django_filters.NumberFilter(
        field_name='car_id__car_id',
        label='Filtrar por ID de cargo'
    )
    cargo_nombre = django_filters.CharFilter(
        field_name='car_id__car_descripcion',
        lookup_expr='icontains',
        label='Filtrar por nombre de cargo'
    )
    distrito_id = django_filters.NumberFilter(
        field_name='dis_id__dis_id',
        label='Filtrar por ID de distrito'
    )
    zona_id = django_filters.NumberFilter(
        field_name='zon_id__zon_id',
        label='Filtrar por ID de zona'
    )
    vigente = django_filters.BooleanFilter(
        field_name='pei_vigente',
        label='Filtrar por vigencia'
    )

    class Meta:
        model = Persona_Individual
        fields = ['persona_run', 'cargo_id', 'cargo_nombre', 'distrito_id', 'zona_id', 'vigente']


class PersonaNivelFilter(django_filters.FilterSet):
    """Filtros para Persona_Nivel"""
    persona_run = django_filters.CharFilter(
        field_name='per_id__per_run',
        lookup_expr='iexact',
        label='Filtrar por RUN'
    )
    nivel_id = django_filters.NumberFilter(
        field_name='niv_id__niv_id',
        label='Filtrar por ID de nivel'
    )
    nivel_nombre = django_filters.CharFilter(
        field_name='niv_id__niv_descripcion',
        lookup_expr='icontains',
        label='Filtrar por nombre de nivel'
    )
    rama_id = django_filters.NumberFilter(
        field_name='ram_id__ram_id',
        label='Filtrar por ID de rama'
    )
    rama_nombre = django_filters.CharFilter(
        field_name='ram_id__ram_descripcion',
        lookup_expr='icontains',
        label='Filtrar por nombre de rama'
    )

    class Meta:
        model = Persona_Nivel
        fields = ['persona_run', 'nivel_id', 'nivel_nombre', 'rama_id', 'rama_nombre']


class PersonaEstadoCursoFilter(django_filters.FilterSet):
    """Filtros para Persona_Estado_Curso"""
    usuario_id = django_filters.NumberFilter(
        field_name='usu_id__usu_id',
        label='Filtrar por ID de usuario'
    )
    persona_run = django_filters.CharFilter(
        field_name='pec_id__per_id__per_run',
        lookup_expr='iexact',
        label='Filtrar por RUN de persona'
    )
    curso_codigo = django_filters.CharFilter(
        field_name='pec_id__cus_id__cur_id__cur_codigo',
        lookup_expr='iexact',
        label='Filtrar por código de curso'
    )
    estado = django_filters.NumberFilter(
        field_name='peu_estado',
        label='Filtrar por estado'
    )
    fecha = django_filters.DateFromToRangeFilter(
        field_name='peu_fecha_hora',
        label='Rango de fecha/hora'
    )
    vigente = django_filters.BooleanFilter(
        field_name='peu_vigente',
        label='Filtrar por vigencia'
    )

    class Meta:
        model = Persona_Estado_Curso
        fields = ['usuario_id', 'persona_run', 'curso_codigo', 'estado', 'fecha', 'vigente']


class PersonaVehiculoFilter(django_filters.FilterSet):
    """Filtros para Persona_Vehiculo"""
    persona_run = django_filters.CharFilter(
        field_name='pec_id__per_id__per_run',
        lookup_expr='iexact',
        label='Filtrar por RUN de persona'
    )
    marca = django_filters.CharFilter(
        field_name='pev_marca',
        lookup_expr='icontains',
        label='Filtrar por marca'
    )
    modelo = django_filters.CharFilter(
        field_name='pev_modelo',
        lookup_expr='icontains',
        label='Filtrar por modelo'
    )
    patente = django_filters.CharFilter(
        field_name='pev_patente',
        lookup_expr='icontains',
        label='Filtrar por patente'
    )

    class Meta:
        model = Persona_Vehiculo
        fields = ['persona_run', 'marca', 'modelo', 'patente']