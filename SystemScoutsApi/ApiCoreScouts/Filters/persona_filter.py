import django_filters
from ..Models.persona_model import *

class PersonaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='PER_NOMBRES',lookup_expr='icontains',
        label='Filtrar por nombre')
    apellido = django_filters.CharFilter(field_name='PER_APELPTA',lookup_expr='icontains',
        label='Filtrar por apellido')
    run = django_filters.CharFilter(field_name='PER_RUN',lookup_expr='exact',
        label='Filtrar por RUN')
    dv = django_filters.CharFilter(field_name='PER_DV',lookup_expr='iexact',
        label='Filtrar por dígito verificador')
    comuna_nombre = django_filters.CharFilter(field_name='COM_ID__COM_DESCRIPCION',lookup_expr='icontains',
        label='Filtrar por nombre de comuna')
    comuna_id = django_filters.NumberFilter(field_name='COM_ID__COM_ID',
        label='Filtrar por ID de comuna')
    usuario_nombre = django_filters.CharFilter(field_name='USU_ID__USU_USERNAME',lookup_expr='icontains',
        label='Filtrar por nombre de usuario')
    usuario_id = django_filters.NumberFilter(field_name='USU_ID__USU_ID',
        label='Filtrar por ID de usuario')
    vigente = django_filters.BooleanFilter(field_name='PER_VIGENTE',
        label='Filtrar por vigencia')

    class Meta:
        model = Persona
        fields = ['nombre',
                  'apellido',
                  'run',
                  'dv',
                  'comuna_nombre',
                  'comuna_id',
                  'usuario_nombre',
                  'usuario_id',
                  'vigente'
                  ]


class PersonaCursoFilter(django_filters.FilterSet):
    """
    Filtros para Persona_Curso, con soporte para búsqueda profunda
    en Persona, Curso_Seccion, Curso, Rol, Alimentación y Nivel.
    """

    # --- Filtros sobre Persona ---
    run = django_filters.CharFilter(
        field_name='PER_ID__PER_RUN',
        lookup_expr='iexact',
        label='Filtrar por RUN (sin DV)'
    )
    dv = django_filters.CharFilter(
        field_name='PER_ID__PER_DV',
        lookup_expr='iexact',
        label='Filtrar por dígito verificador'
    )
    nombre_persona = django_filters.CharFilter(
        field_name='PER_ID__PER_NOMBRES',
        lookup_expr='icontains',
        label='Filtrar por nombre de persona'
    )
    apellido_persona = django_filters.CharFilter(
        field_name='PER_ID__PER_APELPTA',
        lookup_expr='icontains',
        label='Filtrar por apellido de persona'
    )

    # --- Filtro sobre Curso ---
    curso_codigo = django_filters.CharFilter(
        field_name='CUS_ID__CUR_ID__CUR_CODIGO',
        lookup_expr='iexact',
        label='Filtrar por código de curso (ej: CUR-0778)'
    )

    # --- Filtros sobre relaciones directas ---
    rol_nombre = django_filters.CharFilter(
        field_name='ROL_ID__ROL_DESCRIPCION',
        lookup_expr='icontains',
        label='Filtrar por nombre de rol'
    )
    alimentacion_nombre = django_filters.CharFilter(
        field_name='ALI_ID__ALI_DESCRIPCION',
        lookup_expr='icontains',
        label='Filtrar por tipo de alimentación'
    )
    nivel_nombre = django_filters.CharFilter(
        field_name='NIV_ID__NIV_DESCRIPCION',
        lookup_expr='icontains',
        label='Filtrar por nivel'
    )

    # --- Filtros booleanos ---
    registrado = django_filters.BooleanFilter(
        field_name='PEC_REGISTRO',
        label='Filtrar por registro completado'
    )
    acreditado = django_filters.BooleanFilter(
        field_name='PEC_ACREDITACION',
        label='Filtrar por acreditación'
    )
    correo_qr_enviado = django_filters.BooleanFilter(
        field_name='PEC_ENVIO_CORREO_QR',
        label='Filtrar por correo QR enviado'
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
        ]


class PersonaGrupoFilter(django_filters.FilterSet):
    """Filtros para Persona_Grupo"""
    persona_run = django_filters.CharFilter(
        field_name='PER_ID__PER_RUN',
        lookup_expr='iexact',
        label='Filtrar por RUN de persona'
    )
    grupo_id = django_filters.NumberFilter(
        field_name='GRU_ID__GRU_ID',
        label='Filtrar por ID de grupo'
    )
    grupo_nombre = django_filters.CharFilter(
        field_name='GRU_ID__GRU_DESCRIPCION',
        lookup_expr='icontains',
        label='Filtrar por nombre de grupo'
    )
    vigente = django_filters.BooleanFilter(
        field_name='PEG_VIGENTE',
        label='Filtrar por vigencia'
    )

    class Meta:
        model = Persona_Grupo
        fields = ['persona_run', 'grupo_id', 'grupo_nombre', 'vigente']


class PersonaFormadorFilter(django_filters.FilterSet):
    """Filtros para Persona_Formador"""
    persona_run = django_filters.CharFilter(
        field_name='PER_ID__PER_RUN',
        lookup_expr='iexact',
        label='Filtrar por RUN de persona'
    )
    persona_nombre = django_filters.CharFilter(
        field_name='PER_ID__PER_NOMBRES',
        lookup_expr='icontains',
        label='Filtrar por nombre'
    )
    habilidad_1 = django_filters.BooleanFilter(
        field_name='PEF_HAB_1',
        label='Tiene habilidad 1'
    )
    habilidad_2 = django_filters.BooleanFilter(
        field_name='PEF_HAB_2',
        label='Tiene habilidad 2'
    )
    verificado = django_filters.BooleanFilter(
        field_name='PEF_VERIF',
        label='Filtrar por verificación'
    )

    class Meta:
        model = Persona_Formador
        fields = ['persona_run', 'persona_nombre', 'habilidad_1', 'habilidad_2', 'verificado']


class PersonaIndividualFilter(django_filters.FilterSet):
    """Filtros para Persona_Individual"""
    persona_run = django_filters.CharFilter(
        field_name='PER_ID__PER_RUN',
        lookup_expr='iexact',
        label='Filtrar por RUN'
    )
    cargo_id = django_filters.NumberFilter(
        field_name='CAR_ID__CAR_ID',
        label='Filtrar por ID de cargo'
    )
    cargo_nombre = django_filters.CharFilter(
        field_name='CAR_ID__CAR_DESCRIPCION',
        lookup_expr='icontains',
        label='Filtrar por nombre de cargo'
    )
    distrito_id = django_filters.NumberFilter(
        field_name='DIS_ID__DIS_ID',
        label='Filtrar por ID de distrito'
    )
    zona_id = django_filters.NumberFilter(
        field_name='ZON_ID__ZON_ID',
        label='Filtrar por ID de zona'
    )
    vigente = django_filters.BooleanFilter(
        field_name='PEI_VIGENTE',
        label='Filtrar por vigencia'
    )

    class Meta:
        model = Persona_Individual
        fields = ['persona_run', 'cargo_id', 'cargo_nombre', 'distrito_id', 'zona_id', 'vigente']


class PersonaNivelFilter(django_filters.FilterSet):
    """Filtros para Persona_Nivel"""
    persona_run = django_filters.CharFilter(
        field_name='PER_ID__PER_RUN',
        lookup_expr='iexact',
        label='Filtrar por RUN'
    )
    nivel_id = django_filters.NumberFilter(
        field_name='NIV_ID__NIV_ID',
        label='Filtrar por ID de nivel'
    )
    nivel_nombre = django_filters.CharFilter(
        field_name='NIV_ID__NIV_DESCRIPCION',
        lookup_expr='icontains',
        label='Filtrar por nombre de nivel'
    )
    rama_id = django_filters.NumberFilter(
        field_name='RAM_ID__RAM_ID',
        label='Filtrar por ID de rama'
    )
    rama_nombre = django_filters.CharFilter(
        field_name='RAM_ID__RAM_DESCRIPCION',
        lookup_expr='icontains',
        label='Filtrar por nombre de rama'
    )

    class Meta:
        model = Persona_Nivel
        fields = ['persona_run', 'nivel_id', 'nivel_nombre', 'rama_id', 'rama_nombre']


class PersonaEstadoCursoFilter(django_filters.FilterSet):
    """Filtros para Persona_Estado_Curso"""
    usuario_id = django_filters.NumberFilter(
        field_name='USU_ID__USU_ID',
        label='Filtrar por ID de usuario'
    )
    persona_run = django_filters.CharFilter(
        field_name='PEC_ID__PER_ID__PER_RUN',
        lookup_expr='iexact',
        label='Filtrar por RUN de persona'
    )
    curso_codigo = django_filters.CharFilter(
        field_name='PEC_ID__CUS_ID__CUR_ID__CUR_CODIGO',
        lookup_expr='iexact',
        label='Filtrar por código de curso'
    )
    estado = django_filters.NumberFilter(
        field_name='PEU_ESTADO',
        label='Filtrar por estado'
    )
    fecha = django_filters.DateFromToRangeFilter(
        field_name='PEU_FECHA_HORA',
        label='Rango de fecha/hora'
    )
    vigente = django_filters.BooleanFilter(
        field_name='PEU_VIGENTE',
        label='Filtrar por vigencia'
    )

    class Meta:
        model = Persona_Estado_Curso
        fields = ['usuario_id', 'persona_run', 'curso_codigo', 'estado', 'fecha', 'vigente']


class PersonaVehiculoFilter(django_filters.FilterSet):
    """Filtros para Persona_Vehiculo"""
    persona_run = django_filters.CharFilter(
        field_name='PEC_ID__PER_ID__PER_RUN',
        lookup_expr='iexact',
        label='Filtrar por RUN de persona'
    )
    marca = django_filters.CharFilter(
        field_name='PEV_MARCA',
        lookup_expr='icontains',
        label='Filtrar por marca'
    )
    modelo = django_filters.CharFilter(
        field_name='PEV_MODELO',
        lookup_expr='icontains',
        label='Filtrar por modelo'
    )
    patente = django_filters.CharFilter(
        field_name='PEV_PATENTE',
        lookup_expr='icontains',
        label='Filtrar por patente'
    )

    class Meta:
        model = Persona_Vehiculo
        fields = ['persona_run', 'marca', 'modelo', 'patente']