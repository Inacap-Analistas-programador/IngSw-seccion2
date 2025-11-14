from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..Views.Persona_view import *

router = DefaultRouter()
router.register(r'personas', PersonaViewSet, basename='persona')
router.register(r'grupos', PersonaGrupoViewSet, basename='persona-grupo')
router.register(r'formadores', PersonaFormadorViewSet, basename='persona-formador')
router.register(r'individuales', PersonaIndividualViewSet, basename='persona-individual')
router.register(r'niveles', PersonaNivelViewSet, basename='persona-nivel')
router.register(r'cursos', PersonaCursoViewSet, basename='persona-curso')
router.register(r'estado-cursos', PersonaEstadoCursoViewSet, basename='persona-estado-curso')
router.register(r'vehiculos', PersonaVehiculoViewSet, basename='persona-vehiculo')

urlpatterns = router.urls