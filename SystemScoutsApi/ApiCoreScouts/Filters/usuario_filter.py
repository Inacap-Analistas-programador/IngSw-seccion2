import django_filters
from ApiCoreScouts.models import *
from rest_framework import viewsets
from ApiCoreScouts.Serializers import UsuarioSerializer
from django_filters.rest_framework import DjangoFilterBackend


# === Filtro para la tabla Usuario === #
class UsuarioFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='USU_USERNAME', lookup_expr='icontains')
    perfil = django_filters.NumberFilter(field_name='PEL_ID__PEL_ID')
    vigente = django_filters.BooleanFilter(field_name='USU_VIGENTE')
    
    class Meta:
        model = Usuario
        fields = ['username', 'perfil', 'vigente']

# === Filtro para la tabla Perfil === #
class PerfilFilter(django_filters.FilterSet):
    descripcion = django_filters.CharFilter(field_name='PEL_DESCRIPCION', lookup_expr='icontains')
    vigente = django_filters.BooleanFilter(field_name='PEL_VIGENTE')

    class Meta:
        model = Perfil
        fields = ['descripcion', 'vigente']

# === Filtro para la tabla Aplicación === #
class AplicacionFilter(django_filters.FilterSet):
    descripcion = django_filters.CharFilter(field_name='APL_DESCRIPCION', lookup_expr='icontains')
    vigente = django_filters.BooleanFilter(field_name='APL_VIGENTE')

    class Meta:
        model = Aplicacion
        fields = ['descripcion', 'vigente']

# === Filtro para la tabla perfil_aplicación === #
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsuarioFilter