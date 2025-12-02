import django_filters
from ..Models.mantenedor_model import *

class RolFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='rol_descripcion', lookup_expr='icontains')
	tipo = django_filters.NumberFilter(field_name='rol_tipo')
	vigente = django_filters.BooleanFilter(field_name='rol_vigente')

	class Meta:
		model = Rol
		fields = ['descripcion', 'tipo', 'vigente']

class CargoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='car_descripcion', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='car_vigente')

	class Meta:
		model = Cargo
		fields = ['descripcion', 'vigente']


class NivelFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='niv_descripcion', lookup_expr='icontains')
	orden = django_filters.NumberFilter(field_name='niv_orden')
	vigente = django_filters.BooleanFilter(field_name='niv_vigente')

	class Meta:
		model = Nivel
		fields = ['descripcion', 'orden', 'vigente']

class ComunaFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='com_descripcion', lookup_expr='icontains')
	provincia_id = django_filters.NumberFilter(field_name='pro_id__pro_id')
	vigente = django_filters.BooleanFilter(field_name='com_vigente')

	class Meta:
		model = Comuna
		fields = ['descripcion', 'provincia_id', 'vigente']

class TipoCursoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='tcu_descripcion', lookup_expr='icontains')
	tipo = django_filters.NumberFilter(field_name='tcu_tipo')
	vigente = django_filters.BooleanFilter(field_name='tcu_vigente')

	class Meta:
		model = Tipo_Curso
		fields = ['descripcion', 'tipo', 'vigente']

class RamaFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='ram_descripcion', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='ram_vigente')

	class Meta:
		model = Rama
		fields = ['descripcion', 'vigente']

class EstadoCivilFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='esc_descripcion', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='esc_vigente')

	class Meta:
		model = Estado_Civil
		fields = ['descripcion', 'vigente']

class ZonaFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='zon_descripcion', lookup_expr='icontains')
	unilateral = django_filters.BooleanFilter(field_name='zon_unilateral')
	vigente = django_filters.BooleanFilter(field_name='zon_vigente')

	class Meta:
		model = Zona
		fields = ['descripcion', 'unilateral', 'vigente']

class DistritoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='dis_descripcion', lookup_expr='icontains')
	zona_id = django_filters.NumberFilter(field_name='zon_id__zon_id')
	vigente = django_filters.BooleanFilter(field_name='dis_vigente')

	class Meta:
		model = Distrito
		fields = ['descripcion', 'zona_id', 'vigente']

class GrupoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='gru_descripcion', lookup_expr='icontains')
	distrito_id = django_filters.NumberFilter(field_name='dis_id__dis_id')
	vigente = django_filters.BooleanFilter(field_name='gru_vigente')

	class Meta:
		model = Grupo
		fields = ['descripcion', 'distrito_id', 'vigente']

class RegionFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='reg_descripcion', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='reg_vigente')

	class Meta:
		model = Region
		fields = ['descripcion', 'vigente']

class ProvinciaFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='pro_descripcion', lookup_expr='icontains')
	region_id = django_filters.NumberFilter(field_name='reg_id__reg_id')
	vigente = django_filters.BooleanFilter(field_name='pro_vigente')

	class Meta:
		model = Provincia
		fields = ['descripcion', 'region_id', 'vigente']

class AlimentacionFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='ali_descripcion', lookup_expr='icontains')
	tipo = django_filters.NumberFilter(field_name='ali_tipo')
	vigente = django_filters.BooleanFilter(field_name='ali_vigente')

	class Meta:
		model = Alimentacion
		fields = ['descripcion', 'tipo', 'vigente']

class ConceptoContableFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='coc_descripcion', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='coc_vigente')

	class Meta:
		model = Concepto_Contable
		fields = ['descripcion', 'vigente']

class TipoArchivoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='tar_descripcion', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='tar_vigente')

	class Meta:
		model = Tipo_Archivo
		fields = ['descripcion', 'vigente']