from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..Views.Usuario_view import UsuarioViewSet, GroupViewSet, PermissionViewSet, GroupWithAmbitoViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'perfiles', GroupViewSet, basename='perfil')
router.register(r'aplicaciones', PermissionViewSet, basename='aplicacion')
router.register(r'perfiles-ambito', GroupWithAmbitoViewSet, basename='perfil-ambito')

urlpatterns = router.urls