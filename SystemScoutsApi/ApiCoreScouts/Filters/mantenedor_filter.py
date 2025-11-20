import django_filters
from ..Models.mantenedor_model import *

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

class RamaFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='RAM_DESCRIPCION', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='RAM_VIGENTE')

	class Meta:
		model = Rama
		fields = ['descripcion', 'vigente']

class EstadoCivilFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='ESC_DESCRIPCION', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='ESC_VIGENTE')

	class Meta:
		model = Estado_Civil
		fields = ['descripcion', 'vigente']

class ZonaFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='ZON_DESCRIPCION', lookup_expr='icontains')
	unilateral = django_filters.BooleanFilter(field_name='ZON_UNILATERAL')
	vigente = django_filters.BooleanFilter(field_name='ZON_VIGENTE')

	class Meta:
		model = Zona
		fields = ['descripcion', 'unilateral', 'vigente']

class DistritoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='DIS_DESCRIPCION', lookup_expr='icontains')
	zona_id = django_filters.NumberFilter(field_name='ZON_ID__ZON_ID')
	vigente = django_filters.BooleanFilter(field_name='DIS_VIGENTE')

	class Meta:
		model = Distrito
		fields = ['descripcion', 'zona_id', 'vigente']

class GrupoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='GRU_DESCRIPCION', lookup_expr='icontains')
	distrito_id = django_filters.NumberFilter(field_name='DIS_ID__DIS_ID')
	vigente = django_filters.BooleanFilter(field_name='GRU_VIGENTE')

	class Meta:
		model = Grupo
		fields = ['descripcion', 'distrito_id', 'vigente']

class RegionFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='REG_DESCRIPCION', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='REG_VIGENTE')

	class Meta:
		model = Region
		fields = ['descripcion', 'vigente']

class ProvinciaFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='PRO_DESCRIPCION', lookup_expr='icontains')
	region_id = django_filters.NumberFilter(field_name='REG_ID__REG_ID')
	vigente = django_filters.BooleanFilter(field_name='PRO_VIGENTE')

	class Meta:
		model = Provincia
		fields = ['descripcion', 'region_id', 'vigente']

class AlimentacionFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='ALI_DESCRIPCION', lookup_expr='icontains')
	tipo = django_filters.NumberFilter(field_name='ALI_TIPO')
	vigente = django_filters.BooleanFilter(field_name='ALI_VIGENTE')

	class Meta:
		model = Alimentacion
		fields = ['descripcion', 'tipo', 'vigente']

class ConceptoContableFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='COC_DESCRIPCION', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='COC_VIGENTE')

	class Meta:
		model = Concepto_Contable
		fields = ['descripcion', 'vigente']

class TipoArchivoFilter(django_filters.FilterSet):
	descripcion = django_filters.CharFilter(field_name='TAR_DESCRIPCION', lookup_expr='icontains')
	vigente = django_filters.BooleanFilter(field_name='TAR_VIGENTE')

	class Meta:
		model = Tipo_Archivo
		fields = ['descripcion', 'vigente']