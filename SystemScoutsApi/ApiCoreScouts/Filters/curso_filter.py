import django_filters
from ..Models.curso_model import *


class CursoFilter(django_filters.FilterSet):
	codigo = django_filters.CharFilter(field_name='cur_codigo', lookup_expr='icontains')
	estado = django_filters.NumberFilter(field_name='cur_estado')
	fecha_solicitud = django_filters.DateFromToRangeFilter(field_name='cur_fecha_solicitud')
	lugar_comuna = django_filters.CharFilter(field_name='com_id_lugar__com_descripcion', lookup_expr='icontains')
	tipo_curso = django_filters.NumberFilter(field_name='tcu_id__tcu_id')
	administra = django_filters.NumberFilter(field_name='cur_administra')

	class Meta:
		model = Curso
		fields = ['codigo', 'estado', 'fecha_solicitud', 'lugar_comuna', 'tipo_curso', 'administra']

class CursoCuotaFilter(django_filters.FilterSet):
	cur_id = django_filters.NumberFilter(field_name='cur_id')
	tipo = django_filters.NumberFilter(field_name='cuu_tipo')
	fecha = django_filters.DateFromToRangeFilter(field_name='cuu_fecha')
	valor = django_filters.RangeFilter(field_name='cuu_valor')

	class Meta:
		model = Curso_Cuota
		fields = ['cur_id', 'tipo', 'fecha', 'valor']

class CursoFechaFilter(django_filters.FilterSet):
	cur_id = django_filters.NumberFilter(field_name='cur_id')
	fecha_inicio = django_filters.DateFromToRangeFilter(field_name='cuf_fecha_inicio')
	fecha_termino = django_filters.DateFromToRangeFilter(field_name='cuf_fecha_termino')
	tipo = django_filters.NumberFilter(field_name='cuf_tipo')

	class Meta:
		model = Curso_Fecha
		fields = ['cur_id', 'fecha_inicio', 'fecha_termino', 'tipo']

class CursoAlimentacionFilter(django_filters.FilterSet):
	cur_id = django_filters.NumberFilter(field_name='cur_id')

	class Meta:
		model = Curso_Alimentacion
		fields = ['cur_id']

class CursoCoordinadorFilter(django_filters.FilterSet):
	cur_id = django_filters.NumberFilter(field_name='cur_id')
	persona_id = django_filters.NumberFilter(field_name='per_id__per_id')
	cargo_id = django_filters.NumberFilter(field_name='car_id__car_id')

	class Meta:
		model = Curso_Coordinador
		fields = ['cur_id', 'persona_id', 'cargo_id']

class CursoSeccionFilter(django_filters.FilterSet):
	cur_id = django_filters.NumberFilter(field_name='cur_id')
	seccion = django_filters.NumberFilter(field_name='cus_seccion')

	class Meta:
		model = Curso_Seccion
		fields = ['cur_id', 'seccion']
	
class CursoFormadorFilter(django_filters.FilterSet):
	cur_id = django_filters.NumberFilter(field_name='cur_id')

	class Meta:
		model = Curso_Formador
		fields = ['cur_id']