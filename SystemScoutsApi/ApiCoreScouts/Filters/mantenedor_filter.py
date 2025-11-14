import django_filters
from ApiCoreScouts.Models.mantenedor_model import (
	Rol, Cargo, Rama, Estado_Civil, Nivel, Zona, Distrito,
	Grupo, Region, Provincia, Comuna, Alimentacion, Concepto_Contable,
	Tipo_Curso, Tipo_Archivo
)


class RolFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='ROL_DESCRIPCION', lookup_expr='icontains')
	tipo = django_filters.NumberFilter(field_name='ROL_TIPO')
	vigente = django_filters.BooleanFilter(field_name='ROL_VIGENTE')

	class Meta:
		model = Rol
		fields = ['descripcion', 'tipo', 'vigente']


class CargoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='CAR_DESCRIPCION', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='CAR_VIGENTE')

	class Meta:
		model = Cargo
		fields = ['descripcion', 'vigente']


class NivelFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='NIV_DESCRIPCION', lookup_expr='icontains')
	orden = django_filters.NumberFilter(field_name='NIV_ORDEN')
	vigente = django_filters.BooleanFilter(field_name='NIV_VIGENTE')

	class Meta:
		model = Nivel
		fields = ['descripcion', 'orden', 'vigente']


class ComunaFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='COM_DESCRIPCION', lookup_expr='icontains')
	provincia_id = django_filters.NumberFilter(field_name='PRO_ID__PRO_ID')
	vigente = django_filters.BooleanFilter(field_name='COM_VIGENTE')

	class Meta:
		model = Comuna
		fields = ['descripcion', 'provincia_id', 'vigente']


class TipoCursoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='TCU_DESCRIPCION', lookup_expr='icontains')
	tipo = django_filters.NumberFilter(field_name='TCU_TIPO')
	vigente = django_filters.BooleanFilter(field_name='TCU_VIGENTE')

	class Meta:
		model = Tipo_Curso
		fields = ['descripcion', 'tipo', 'vigente']


class TipoArchivoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='TAR_DESCRIPCION', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='TAR_VIGENTE')

	class Meta:
		model = Tipo_Archivo
		fields = ['descripcion', 'vigente']