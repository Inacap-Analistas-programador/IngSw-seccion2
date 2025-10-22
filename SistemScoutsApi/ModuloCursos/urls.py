from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CursoViewSet, CursoCuotaViewSet, CursoFechaViewSet,
                    CursoAlimentacionViewSet, CursoCoordinadorViewSet,
                    CursoSeccionViewSet, CursoFormadorViewSet,
                    TipoCursoViewSet)

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'curso-cuotas', CursoCuotaViewSet, basename='curso-cuota')
router.register(r'curso-fechas', CursoFechaViewSet, basename='curso-fecha')
router.register(r'curso-alimentaciones', CursoAlimentacionViewSet, basename='curso-alimentacion')
router.register(r'curso-coordinadores', CursoCoordinadorViewSet, basename='curso-coordinador')
router.register(r'curso-secciones', CursoSeccionViewSet, basename='curso-seccion')
router.register(r'curso-formadores', CursoFormadorViewSet, basename='curso-formador')
router.register(r'tipo-cursos', TipoCursoViewSet, basename='tipo-curso')

urlpatterns = [
    path('', include(router.urls)),
]
