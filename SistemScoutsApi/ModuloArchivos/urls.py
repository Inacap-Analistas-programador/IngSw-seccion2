from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ArchivoViewSet, ArchivoCursoViewSet, ArchivoPersonaViewSet, TipoArchivoViewSet

router = DefaultRouter()
router.register(r'archivos', ArchivoViewSet, basename='archivos')
router.register(r'archivo-cursos', ArchivoCursoViewSet, basename='archivo-cursos')
router.register(r'archivo-personas', ArchivoPersonaViewSet, basename='archivo-personas')
router.register(r'tipo-archivos', TipoArchivoViewSet, basename='tipo-archivos')

urlpatterns = [
    path('', include(router.urls)),
]
