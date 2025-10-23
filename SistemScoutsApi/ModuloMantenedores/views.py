from rest_framework import viewsets
from ApiCore.serializers import ModuloMantenedoresSerializers
from .models import (Alimentacion, Comuna, Provincia, Rol, Cargo, Rama, Estado_Civil,
                            Nivel, Zona, Distrito, Grupo, Region)

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = ModuloMantenedoresSerializers.RolSerializer

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = ModuloMantenedoresSerializers.CargoSerializer

class RamaViewSet(viewsets.ModelViewSet):
    queryset = Rama.objects.all()
    serializer_class = ModuloMantenedoresSerializers.RamaSerializer

class EstadoCivilViewSet(viewsets.ModelViewSet):
    queryset = Estado_Civil.objects.all()
    serializer_class = ModuloMantenedoresSerializers.EstadoCivilSerializer

class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = ModuloMantenedoresSerializers.NivelSerializer

class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ModuloMantenedoresSerializers.ZonaSerializer

class DistritoViewSet(viewsets.ModelViewSet):
    queryset = Distrito.objects.all()
    serializer_class = ModuloMantenedoresSerializers.DistritoSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = ModuloMantenedoresSerializers.GrupoSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = ModuloMantenedoresSerializers.RegionSerializer

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ModuloMantenedoresSerializers.ProvinciaSerializer

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ModuloMantenedoresSerializers.ComunaSerializer

class AlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Alimentacion.objects.all()
    serializer_class = ModuloMantenedoresSerializers.AlimentacionSerializer

