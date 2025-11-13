import django_filters
from ApiCoreScouts.Models.usuario_model import Usuario, Perfil, Aplicacion, Perfil_Aplicacion

"""
Filtros relacionados con usuarios y permisos.

Este módulo contiene FilterSets para:
- Usuario: búsqueda por username, perfil y vigencia.
- Perfil: búsqueda por descripción y vigencia.
- Aplicacion: búsqueda por descripción y vigencia.
- Perfil_Aplicacion: filtros para la relación Perfil <-> Aplicacion
  (buscar por id/descripcion de perfil y aplicación y por permisos booleans).

Los nombres de los parámetros de consulta son descriptivos y usan
`lookup_expr='icontains'` o comparaciones exactas según convenga.
"""


class UsuarioFilter(django_filters.FilterSet):
    """Filtro para la tabla Usuario.

    Parámetros disponibles:
    - username: búsqueda parcial sobre `USU_USERNAME` (icontains)
    - perfil: id del perfil (`PEL_ID`)
    - vigente: booleano sobre `USU_VIGENTE`
    """
    username = django_filters.CharFilter(field_name='USU_USERNAME', lookup_expr='icontains', label='Filtrar por username')
    perfil = django_filters.NumberFilter(field_name='PEL_ID__PEL_ID', label='Filtrar por ID de perfil')
    vigente = django_filters.BooleanFilter(field_name='USU_VIGENTE', label='Filtrar por vigencia del usuario')

    class Meta:
        model = Usuario
        fields = ['username', 'perfil', 'vigente']


class PerfilFilter(django_filters.FilterSet):
    """Filtro para la tabla Perfil (roles/perfiles).

    Parámetros:
    - descripcion: búsqueda parcial sobre `PEL_DESCRIPCION`
    - vigente: booleano sobre `PEL_VIGENTE`
    """
    descripcion = django_filters.CharFilter(field_name='PEL_DESCRIPCION', lookup_expr='icontains', label='Filtrar por descripción de perfil')
    vigente = django_filters.BooleanFilter(field_name='PEL_VIGENTE', label='Filtrar por vigencia del perfil')

    class Meta:
        model = Perfil
        fields = ['descripcion', 'vigente']


class AplicacionFilter(django_filters.FilterSet):
    """Filtro para la tabla Aplicacion.

    Parámetros:
    - descripcion: búsqueda parcial sobre `APL_DESCRIPCION`
    - vigente: booleano sobre `APL_VIGENTE`
    """
    descripcion = django_filters.CharFilter(field_name='APL_DESCRIPCION', lookup_expr='icontains', label='Filtrar por descripción de aplicación')
    vigente = django_filters.BooleanFilter(field_name='APL_VIGENTE', label='Filtrar por vigencia de la aplicación')

    class Meta:
        model = Aplicacion
        fields = ['descripcion', 'vigente']


class PerfilAplicacionFilter(django_filters.FilterSet):
    """Filtros para la relación Perfil_Aplicacion.

    Permite filtrar por perfil, aplicación y por los permisos booleanos
    (ingresar/modificar/eliminar/consultar).
    """
    perfil_id = django_filters.NumberFilter(field_name='PEL_ID__PEL_ID', label='ID de perfil')
    perfil_descripcion = django_filters.CharFilter(field_name='PEL_ID__PEL_DESCRIPCION', lookup_expr='icontains', label='Descripción del perfil')
    aplicacion_id = django_filters.NumberFilter(field_name='APL_ID__APL_ID', label='ID de aplicación')
    aplicacion_descripcion = django_filters.CharFilter(field_name='APL_ID__APL_DESCRIPCION', lookup_expr='icontains', label='Descripción de la aplicación')
    ingresar = django_filters.BooleanFilter(field_name='PEA_INGRESAR', label='Permiso ingresar')
    modificar = django_filters.BooleanFilter(field_name='PEA_MODIFICAR', label='Permiso modificar')
    eliminar = django_filters.BooleanFilter(field_name='PEA_ELIMINAR', label='Permiso eliminar')
    consultar = django_filters.BooleanFilter(field_name='PEA_CONSULTAR', label='Permiso consultar')

    class Meta:
        model = Perfil_Aplicacion
        fields = [
            'perfil_id',
            'perfil_descripcion',
            'aplicacion_id',
            'aplicacion_descripcion',
            'ingresar',
            'modificar',
            'eliminar',
            'consultar',
        ]
