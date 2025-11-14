import django_filters
from ApiCoreScouts.Models.archivo_model import Archivo, Archivo_Curso, Archivo_Persona


class ArchivoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='ARC_DESCRIPCION', lookup_expr='icontains')
	tipo_descripcion = django_filters.CharFilter(field_name='TAR_ID__TAR_DESCRIPCION', lookup_expr='icontains')
	usuario_crea = django_filters.CharFilter(field_name='USU_ID_CREA__USU_USERNAME', lookup_expr='icontains')
	fecha = django_filters.DateFromToRangeFilter(field_name='ARC_FECHA_HORA')
	vigente = django_filters.BooleanFilter(field_name='ARC_VIGENTE')

	class Meta:
		model = Archivo
		fields = ['descripcion', 'tipo_descripcion', 'usuario_crea', 'fecha', 'vigente']


class ArchivoCursoFilter(django_filters.FilterSet):
	archivo_id = django_filters.NumberFilter(field_name='ARC_ID__ARC_ID')
	seccion_id = django_filters.NumberFilter(field_name='CUS_ID__CUS_ID')

	class Meta:
		model = Archivo_Curso
		fields = ['archivo_id', 'seccion_id']


class ArchivoPersonaFilter(django_filters.FilterSet):
	archivo_id = django_filters.NumberFilter(field_name='ARC_ID__ARC_ID')
	persona_id = django_filters.NumberFilter(field_name='PER_ID__PER_ID')
	seccion_id = django_filters.NumberFilter(field_name='CUS_ID__CUS_ID')

	class Meta:
		model = Archivo_Persona
		fields = ['archivo_id', 'persona_id', 'seccion_id']