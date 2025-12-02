import django_filters
from ..Models.usuario_model import *


class UsuarioFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='usu_username', lookup_expr='icontains')
    perfil = django_filters.NumberFilter(field_name='pel_id__pel_id')
    vigente = django_filters.BooleanFilter(field_name='usu_vigente')
    
    class Meta:
        model = Usuario
        fields = ['username', 'perfil', 'vigente']


class PerfilFilter(django_filters.FilterSet):
    descripcion = django_filters.CharFilter(field_name='pel_descripcion', lookup_expr='icontains')
    vigente = django_filters.BooleanFilter(field_name='pel_vigente')

    class Meta:
        model = Perfil
        fields = ['descripcion', 'vigente']


class AplicacionFilter(django_filters.FilterSet):
    descripcion = django_filters.CharFilter(field_name='apl_descripcion', lookup_expr='icontains')
    vigente = django_filters.BooleanFilter(field_name='apl_vigente')

    class Meta:
        model = Aplicacion
        fields = ['descripcion', 'vigente']

class PerfilAplicacionFilter(django_filters.FilterSet):
    perfil_id = django_filters.NumberFilter(field_name='pel_id__pel_id')
    aplicacion_id = django_filters.NumberFilter(field_name='apl_id__apl_id')

    class Meta:
        model = Perfil_Aplicacion
        fields = ['perfil_id', 'aplicacion_id']