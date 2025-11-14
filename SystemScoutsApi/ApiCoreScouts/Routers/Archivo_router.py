from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ..Views.Archivo_view import *

router = DefaultRouter()
router.register(r'archivos', ArchivoViewSet, basename='archivos')
router.register(r'cursos', ArchivoCursoViewSet, basename='archivo-cursos')
router.register(r'personas', ArchivoPersonaViewSet, basename='archivo-personas')

urlpatterns = router.urls