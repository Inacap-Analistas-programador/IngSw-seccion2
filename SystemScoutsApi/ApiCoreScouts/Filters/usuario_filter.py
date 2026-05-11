import django_filters
from ..Models.usuario_model import Usuario
from django.contrib.auth.models import Group

class UsuarioFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    groups = django_filters.ModelMultipleChoiceFilter(
        field_name='groups__name',
        to_field_name='name',
        queryset=Group.objects.all(),
    )
    is_active = django_filters.BooleanFilter(field_name='is_active')
    
    class Meta:
        model = Usuario
        fields = ['username', 'groups', 'is_active']