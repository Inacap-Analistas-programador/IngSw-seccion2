import django_filters
from ApiCoreScouts.Models.curso_model import Curso, Curso_Seccion, Curso_Fecha, Curso_Cuota


class CursoFilter(django_filters.FilterSet):
	codigo = django_filters.CharFilter(field_name='CUR_CODIGO', lookup_expr='icontains')
	estado = django_filters.NumberFilter(field_name='CUR_ESTADO')
	fecha_solicitud = django_filters.DateFromToRangeFilter(field_name='CUR_FECHA_SOLICITUD')
	lugar_comuna = django_filters.CharFilter(field_name='COM_ID_LUGAR__COM_DESCRIPCION', lookup_expr='icontains')
	tipo_curso = django_filters.NumberFilter(field_name='TCU_ID__TCU_ID')
	administra = django_filters.NumberFilter(field_name='CUR_ADMINISTRA')

	class Meta:
		model = Curso
		fields = ['codigo', 'estado', 'fecha_solicitud', 'lugar_comuna', 'tipo_curso', 'administra']


class CursoSeccionFilter(django_filters.FilterSet):
	curso_id = django_filters.NumberFilter(field_name='CUR_ID__CUR_ID')
	seccion = django_filters.NumberFilter(field_name='CUS_SECCION')

	class Meta:
		model = Curso_Seccion
		fields = ['curso_id', 'seccion']