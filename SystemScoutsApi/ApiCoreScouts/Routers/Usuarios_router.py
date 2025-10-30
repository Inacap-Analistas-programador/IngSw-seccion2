from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..View.Usuario_view import *

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'perfiles', PerfilViewSet, basename='perfil')
router.register(r'aplicaciones', AplicacionViewSet, basename='aplicacion')
router.register(r'perfil-aplicaciones', PerfilAplicacionViewSet, basename='perfil-aplicacion')

urlpatterns = router.urls