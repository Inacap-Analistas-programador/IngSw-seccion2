import django_filters
from ..Models.pago_model import *


class PagoPersonaFilter(django_filters.FilterSet):
	persona_run = django_filters.CharFilter(field_name='PER_ID__PER_RUN', lookup_expr='iexact', label='RUN de la persona')
	curso_id = django_filters.NumberFilter(field_name='CUR_ID__CUR_ID', label='ID del curso')
	usuario_id = django_filters.NumberFilter(field_name='USU_ID__USU_ID', label='ID de usuario')
	tipo = django_filters.NumberFilter(field_name='PAP_TIPO', label='Tipo de pago (1=Ingreso,2=Egreso)')
	estado = django_filters.NumberFilter(field_name='PAP_ESTADO', label='Estado de pago')
	fecha = django_filters.DateFromToRangeFilter(field_name='PAP_FECHA_HORA', label='Rango de fecha/hora')
	valor = django_filters.RangeFilter(field_name='PAP_VALOR', label='Rango de valor')

	class Meta:
		model = Pago_Persona
		fields = ['persona_run', 'curso_id', 'usuario_id', 'tipo', 'estado', 'fecha', 'valor']


class ComprobantePagoFilter(django_filters.FilterSet):
	usuario_id = django_filters.NumberFilter(field_name='USU_ID__USU_ID')
	curso_id = django_filters.NumberFilter(field_name='PEC_ID__CUR_ID')
	numero = django_filters.NumberFilter(field_name='CPA_NUMERO')
	fecha = django_filters.DateFromToRangeFilter(field_name='CPA_FECHA', label='Rango de fecha')
	valor = django_filters.RangeFilter(field_name='CPA_VALOR')

	class Meta:
		model = Comprobante_Pago
		fields = ['usuario_id', 'curso_id', 'numero', 'fecha', 'valor']


class PagoComprobanteFilter(django_filters.FilterSet):
	pago_persona_id = django_filters.NumberFilter(field_name='PAP_ID__PAP_ID', label='ID de pago de persona')
	comprobante_pago_id = django_filters.NumberFilter(field_name='CPA_ID__CPA_ID', label='ID de comprobante de pago')

	class Meta:
		model = Pago_Comprobante
		fields = ['pago_persona_id', 'comprobante_pago_id']


class PrepagoFilter(django_filters.FilterSet):
	persona_id = django_filters.NumberFilter(field_name='PER_ID__PER_ID')
	curso_id = django_filters.NumberFilter(field_name='CUR_ID__CUR_ID')
	valor = django_filters.RangeFilter(field_name='PPA_VALOR')
	vigente = django_filters.BooleanFilter(field_name='PPA_VIGENTE')

	class Meta:
		model = Prepago
		fields = ['persona_id', 'curso_id', 'valor', 'vigente']


class ProveedorFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='PRV_DESCRIPCION', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='PRV_VIGENTE')

	class Meta:
		model = Proveedor
		fields = ['descripcion', 'vigente']