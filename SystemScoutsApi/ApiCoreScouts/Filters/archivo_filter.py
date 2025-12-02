import django_filters
from ..Models.archivo_model import *


class ArchivoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='arc_descripcion', lookup_expr='icontains')
	tipo_descripcion = django_filters.CharFilter(field_name='tar_id__tar_descripcion', lookup_expr='icontains')
	usuario_crea = django_filters.CharFilter(field_name='usu_id_crea__usu_username', lookup_expr='icontains')
	fecha = django_filters.DateFromToRangeFilter(field_name='arc_fecha_hora')
	vigente = django_filters.BooleanFilter(field_name='arc_vigente')

	class Meta:
		model = Archivo
		fields = ['descripcion', 'tipo_descripcion', 'usuario_crea', 'fecha', 'vigente']


class ArchivoCursoFilter(django_filters.FilterSet):
	archivo_id = django_filters.NumberFilter(field_name='arc_id__arc_id')
	seccion_id = django_filters.NumberFilter(field_name='cus_id__cus_id')

	class Meta:
		model = Archivo_Curso
		fields = ['archivo_id', 'seccion_id']


class ArchivoPersonaFilter(django_filters.FilterSet):
	archivo_id = django_filters.NumberFilter(field_name='arc_id__arc_id')
	persona_id = django_filters.NumberFilter(field_name='per_id__per_id')
	seccion_id = django_filters.NumberFilter(field_name='cus_id__cus_id')

	class Meta:
		model = Archivo_Persona
		fields = ['archivo_id', 'persona_id', 'seccion_id']