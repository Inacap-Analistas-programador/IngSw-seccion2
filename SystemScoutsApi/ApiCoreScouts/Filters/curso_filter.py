import django_filters
from ..Models.curso_model import *


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

class CursoCuotaFilter(django_filters.FilterSet):
	curso_id = django_filters.NumberFilter(field_name='CUR_ID__CUR_ID')
	tipo = django_filters.NumberFilter(field_name='CUU_TIPO')
	fecha = django_filters.DateFromToRangeFilter(field_name='CUU_FECHA')
	valor = django_filters.RangeFilter(field_name='CUU_VALOR')

	class Meta:
		model = Curso_Cuota
		fields = ['curso_id', 'tipo', 'fecha', 'valor']

class CursoFechaFilter(django_filters.FilterSet):
	CUR_ID = django_filters.NumberFilter(field_name='CUR_ID')
	fecha_inicio = django_filters.DateFromToRangeFilter(field_name='CUF_FECHA_INICIO')
	fecha_termino = django_filters.DateFromToRangeFilter(field_name='CUF_FECHA_TERMINO')
	tipo = django_filters.NumberFilter(field_name='CUF_TIPO')

	class Meta:
		model = Curso_Fecha
		fields = ['CUR_ID', 'fecha_inicio', 'fecha_termino', 'tipo']

class CursoAlimentacionFilter(django_filters.FilterSet):
	CUR_ID = django_filters.NumberFilter(field_name='CUR_ID')

	class Meta:
		model = Curso_Alimentacion
		fields = ['CUR_ID']

class CursoCoordinadorFilter(django_filters.FilterSet):
	curso_id = django_filters.NumberFilter(field_name='CUR_ID__CUR_ID')
	persona_id = django_filters.NumberFilter(field_name='PER_ID__PER_ID')
	cargo_id = django_filters.NumberFilter(field_name='CAR_ID__CAR_ID')

	class Meta:
		model = Curso_Coordinador
		fields = ['curso_id', 'persona_id', 'cargo_id']

class CursoSeccionFilter(django_filters.FilterSet):
	curso_id = django_filters.NumberFilter(field_name='CUR_ID__CUR_ID')
	seccion = django_filters.NumberFilter(field_name='CUS_SECCION')

	class Meta:
		model = Curso_Seccion
		fields = ['curso_id', 'seccion']
	
class CursoFormadorFilter(django_filters.FilterSet):
	CUR_ID = django_filters.NumberFilter(field_name='CUR_ID')

	class Meta:
		model = Curso_Formador
		fields = ['CUR_ID']