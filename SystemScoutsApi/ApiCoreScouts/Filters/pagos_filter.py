import django_filters
from django.db.models import Q
from ..Models.pago_model import *


class PagoPersonaFilter(django_filters.FilterSet):
	search = django_filters.CharFilter(method='filter_search', label='Búsqueda general (Nombre, Run, Email)')
	persona_run = django_filters.CharFilter(field_name='per_id__per_run', lookup_expr='iexact', label='RUN de la persona')
	curso_id = django_filters.NumberFilter(field_name='cur_id__cur_id', label='ID del curso')
	usuario_id = django_filters.NumberFilter(field_name='usu_id__usu_id', label='ID de usuario')
	tipo = django_filters.NumberFilter(field_name='pap_tipo', label='Tipo de pago (1=Ingreso,2=Egreso)')
	estado = django_filters.NumberFilter(field_name='pap_estado', label='Estado de pago')
	fecha = django_filters.DateFromToRangeFilter(field_name='pap_fecha_hora', label='Rango de fecha/hora')
	valor = django_filters.RangeFilter(field_name='pap_valor', label='Rango de valor')

	class Meta:
		model = Pago_Persona
		fields = ['search', 'persona_run', 'curso_id', 'usuario_id', 'tipo', 'estado', 'fecha', 'valor']

	def filter_search(self, queryset, name, value):
		if not value:
			return queryset
		return queryset.filter(
			Q(per_id__per_nombres__icontains=value) |
			Q(per_id__per_apelpta__icontains=value) |
			Q(per_id__per_run__icontains=value) |
			Q(per_id__per_mail__icontains=value)
		)


class ComprobantePagoFilter(django_filters.FilterSet):
	usuario_id = django_filters.NumberFilter(field_name='usu_id__usu_id')
	curso_id = django_filters.NumberFilter(field_name='pec_id__cur_id')
	numero = django_filters.NumberFilter(field_name='cpa_numero')
	fecha = django_filters.DateFromToRangeFilter(field_name='cpa_fecha', label='Rango de fecha')
	valor = django_filters.RangeFilter(field_name='cpa_valor')

	class Meta:
		model = Comprobante_Pago
		fields = ['usuario_id', 'curso_id', 'numero', 'fecha', 'valor']


class PagoComprobanteFilter(django_filters.FilterSet):
	pago_persona_id = django_filters.NumberFilter(field_name='pap_id__pap_id', label='ID de pago de persona')
	comprobante_pago_id = django_filters.NumberFilter(field_name='cpa_id__cpa_id', label='ID de comprobante de pago')

	class Meta:
		model = Pago_Comprobante
		fields = ['pago_persona_id', 'comprobante_pago_id']


class PrepagoFilter(django_filters.FilterSet):
	persona_id = django_filters.NumberFilter(field_name='per_id__per_id')
	curso_id = django_filters.NumberFilter(field_name='cur_id__cur_id')
	valor = django_filters.RangeFilter(field_name='ppa_valor')
	vigente = django_filters.BooleanFilter(field_name='ppa_vigente')

	class Meta:
		model = Prepago
		fields = ['persona_id', 'curso_id', 'valor', 'vigente']


class ProveedorFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='prv_descripcion', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='prv_vigente')

	class Meta:
		model = Proveedor
		fields = ['descripcion', 'vigente']