from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ..Api_Views.Archivos_view import *

router = DefaultRouter()
router.register(r'archivos', ArchivoViewSet, basename='archivos')
router.register(r'archivo-cursos', ArchivoCursoViewSet, basename='archivo-cursos')
router.register(r'archivo-personas', ArchivoPersonaViewSet, basename='archivo-personas')
router.register(r'tipo-archivos', TipoArchivoViewSet, basename='tipo-archivos')

urlpatterns = router.urls