from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..Api_Views.Usuario_view import *

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'personas', PersonaViewSet, basename='persona')
router.register(r'perfiles', PerfilViewSet, basename='perfil')
router.register(r'aplicaciones', AplicacionViewSet, basename='aplicacion')
router.register(r'persona-grupos', PersonaGrupoViewSet, basename='persona-grupo')
router.register(r'persona-formadores', PersonaFormadorViewSet, basename='persona-formador')
router.register(r'persona-individuales', PersonaIndividualViewSet, basename='persona-individual')
router.register(r'persona-niveles', PersonaNivelViewSet, basename='persona-nivel')
router.register(r'persona-cursos', PersonaCursoViewSet, basename='persona-curso')
router.register(r'persona-estado-cursos', PersonaEstadoCursoViewSet, basename='persona-estado-curso')
router.register(r'persona-vehiculos', PersonaVehiculoViewSet, basename='persona-vehiculo')
router.register(r'perfil-aplicaciones', PerfilAplicacionViewSet, basename='perfil-aplicacion')

urlpatterns = router.urls