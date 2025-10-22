from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AlimentacionViewSet, ComunaViewSet, ProvinciaViewSet, RolViewSet, CargoViewSet, RamaViewSet, EstadoCivilViewSet,
                    NivelViewSet, ZonaViewSet, DistritoViewSet, GrupoViewSet, RegionViewSet)

router = DefaultRouter()
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'cargos', CargoViewSet, basename='cargo')
router.register(r'ramas', RamaViewSet, basename='rama')
router.register(r'estados-civiles', EstadoCivilViewSet, basename='estado_civil')
router.register(r'niveles', NivelViewSet, basename='nivel')
router.register(r'zonas', ZonaViewSet, basename='zona')
router.register(r'distritos', DistritoViewSet, basename='distrito')
router.register(r'grupos', GrupoViewSet, basename='grupo')
router.register(r'regiones', RegionViewSet, basename='region')
router.register(r'provincias', ProvinciaViewSet, basename='provincia')
router.register(r'comunas', ComunaViewSet, basename='comuna')
router.register(r'alimentaciones', AlimentacionViewSet, basename='alimentacion')

urlpatterns = [
    path('', include(router.urls)),
]