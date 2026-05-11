from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..Views.Usuario_view import UsuarioViewSet, GroupViewSet, PermissionViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'perfiles', GroupViewSet, basename='perfil')
router.register(r'aplicaciones', PermissionViewSet, basename='aplicacion')
# perfil-aplicaciones is no longer needed as permissions are directly in groups/users
# router.register(r'perfil-aplicaciones', PerfilAplicacionViewSet, basename='perfil-aplicacion')

urlpatterns = router.urls