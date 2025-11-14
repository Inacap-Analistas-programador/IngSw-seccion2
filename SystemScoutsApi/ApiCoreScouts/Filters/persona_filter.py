import django_filters
from ApiCoreScouts.Models.persona_model import *

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