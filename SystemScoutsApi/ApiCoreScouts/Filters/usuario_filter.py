import django_filters
from ..Models.usuario_model import *


class UsuarioFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='USU_USERNAME', lookup_expr='icontains')
    perfil = django_filters.NumberFilter(field_name='PEL_ID__PEL_ID')
    vigente = django_filters.BooleanFilter(field_name='USU_VIGENTE')
    
    class Meta:
        model = Usuario
        fields = ['username', 'perfil', 'vigente']


class PerfilFilter(django_filters.FilterSet):
    descripcion = django_filters.CharFilter(field_name='PEL_DESCRIPCION', lookup_expr='icontains')
    vigente = django_filters.BooleanFilter(field_name='PEL_VIGENTE')

    class Meta:
        model = Perfil
        fields = ['descripcion', 'vigente']


class AplicacionFilter(django_filters.FilterSet):
    descripcion = django_filters.CharFilter(field_name='APL_DESCRIPCION', lookup_expr='icontains')
    vigente = django_filters.BooleanFilter(field_name='APL_VIGENTE')

    class Meta:
        model = Aplicacion
        fields = ['descripcion', 'vigente']

class PerfilAplicacionFilter(django_filters.FilterSet):
    perfil_id = django_filters.NumberFilter(field_name='PEL_ID__PEL_ID')
    aplicacion_id = django_filters.NumberFilter(field_name='APL_ID__APL_ID')

    class Meta:
        model = Perfil_Aplicacion
        fields = ['perfil_id', 'aplicacion_id']