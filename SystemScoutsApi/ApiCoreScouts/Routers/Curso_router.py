from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..Views.Curso_view import *

router = DefaultRouter()

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'cuotas', CursoCuotaViewSet, basename='curso-cuota')
router.register(r'fechas', CursoFechaViewSet, basename='curso-fecha')
router.register(r'alimentaciones', CursoAlimentacionViewSet, basename='curso-alimentacion')
router.register(r'coordinadores', CursoCoordinadorViewSet, basename='curso-coordinador')
router.register(r'secciones', CursoSeccionViewSet, basename='curso-seccion')
router.register(r'formadores', CursoFormadorViewSet, basename='curso-formador')

urlpatterns = router.urls