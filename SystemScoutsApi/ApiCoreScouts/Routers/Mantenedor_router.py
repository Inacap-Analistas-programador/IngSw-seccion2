from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..Views.Mantenedor_view import *

router = DefaultRouter()
router.register(r'concepto-contable', ConceptoViewSet, basename='concepto-contable')
router.register(r'tipo-cursos', TipoCursoViewSet, basename='tipo-curso')
router.register(r'tipo-archivos', TipoArchivoViewSet, basename='tipo-archivos')
router.register(r'alimentacion', AlimentacionViewSet, basename='alimentacion')
router.register(r'rol', RolViewSet, basename='rol')
router.register(r'cargo', CargoViewSet, basename='cargo')
router.register(r'rama', RamaViewSet, basename='rama')
router.register(r'estado-civil', EstadoCivilViewSet, basename='estado-civil')
router.register(r'nivel', NivelViewSet, basename='nivel')
router.register(r'zona', ZonaViewSet, basename='zona')
router.register(r'distrito', DistritoViewSet, basename='distrito')
router.register(r'grupo', GrupoViewSet, basename='grupo')
router.register(r'region', RegionViewSet, basename='region')
router.register(r'provincia', ProvinciaViewSet, basename='provincia')
router.register(r'comuna', ComunaViewSet, basename='comuna')
