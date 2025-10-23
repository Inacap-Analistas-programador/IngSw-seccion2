from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ModuloUsuarioCurso.views import (
    UsuarioViewSet,
    PersonaViewSet,
    PerfilViewSet,
    AplicacionViewSet,
    PersonaGrupoViewSet,
    PersonaFormadorViewSet,
    PersonaIndividualViewSet,
    PersonaNivelViewSet,
    PersonaCursoViewSet,
    PersonaEstadoCursoViewSet,
    PersonaVehiculoViewSet,
    PerfilAplicacionViewSet,
    CursoViewSet, 
    CursoCuotaViewSet, 
    CursoFechaViewSet,
    CursoAlimentacionViewSet, 
    CursoCoordinadorViewSet,
    CursoSeccionViewSet, 
    CursoFormadorViewSet,
    TipoCursoViewSet
)

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'curso-cuotas', CursoCuotaViewSet, basename='curso-cuota')
router.register(r'curso-fechas', CursoFechaViewSet, basename='curso-fecha')
router.register(r'curso-alimentaciones', CursoAlimentacionViewSet, basename='curso-alimentacion')
router.register(r'curso-coordinadores', CursoCoordinadorViewSet, basename='curso-coordinador')
router.register(r'curso-secciones', CursoSeccionViewSet, basename='curso-seccion')
router.register(r'curso-formadores', CursoFormadorViewSet, basename='curso-formador')
router.register(r'tipo-cursos', TipoCursoViewSet, basename='tipo-curso')
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

urlpatterns = [
    path('', include(router.urls)),
]
