from rest_framework import viewsets
from ..Serializers import Mantenedores_serializers as MP_S
from ..Models.ModuloMantenedores import *

class ConceptoViewSet(viewsets.ModelViewSet):
    queryset = Concepto_Contable.objects.all()
    serializer_class = MP_S.ConceptoContableSerializer

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = MP_S.RolSerializer

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = MP_S.CargoSerializer

class RamaViewSet(viewsets.ModelViewSet):
    queryset = Rama.objects.all()
    serializer_class = MP_S.RamaSerializer

class EstadoCivilViewSet(viewsets.ModelViewSet):
    queryset = Estado_Civil.objects.all()
    serializer_class = MP_S.EstadoCivilSerializer

class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = MP_S.NivelSerializer

class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = MP_S.ZonaSerializer

class DistritoViewSet(viewsets.ModelViewSet):
    queryset = Distrito.objects.all()
    serializer_class = MP_S.DistritoSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = MP_S.GrupoSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = MP_S.RegionSerializer    

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = MP_S.ProvinciaSerializer

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = MP_S.ComunaSerializer

class TipoCursoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Curso.objects.all()
    serializer_class = MP_S.TipoCursoSerializer

class TipoArchivoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Archivo.objects.all()
    serializer_class = MP_S.TipoArchivoSerializer

class AlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Alimentacion.objects.all()
    serializer_class = MP_S.AlimentacionSerializer