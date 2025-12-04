from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.views.static import serve

from ApiCoreScouts.Routers.Usuario_router import router as usuario_router
from ApiCoreScouts.Routers.Curso_router import router as curso_router
from ApiCoreScouts.Routers.Archivo_router import router as archivo_router
from ApiCoreScouts.Routers.Pago_router import router as pago_router
from ApiCoreScouts.Routers.Mantenedor_router import router as mantenedor_router
from ApiCoreScouts.Routers.Persona_router import router as personas_router

from rest_framework_simplejwt.views import TokenRefreshView
from ApiCoreScouts.Views.Usuario_view import MyTokenObtainPairView

from ApiCoreScouts.Views.Verificador_view import verificar_acreditacion_qr
from ApiCoreScouts.Views.Health_view import CheckView as cv
from ApiCoreScouts.Views.Security_view import SLVS, SCV
from rest_framework.routers import DefaultRouter

sec_rt = DefaultRouter()
sec_rt.register(r'logs', SLVS)

# activar el renderizado si existe el frontend
# FRONTEND_DIST_EXISTS = True 
urlpatterns = [
    path('api/health/', cv.as_view(), name='health_check'),
    path('api/security/', include(sec_rt.urls)),
    path('api/security/check/', SCV.as_view(), name='security_check'),
    path('api/usuarios/', include(usuario_router.urls)),
    path('api/personas/', include(personas_router.urls)),
    path('api/cursos/', include(curso_router.urls)),
    path('api/archivos/', include(archivo_router.urls)),
    path('api/mantenedores/', include(mantenedor_router.urls)),
    path('api/pagos/', include(pago_router.urls)),
    path('api/verificar-qr/', verificar_acreditacion_qr, name='verificar_qr'),
    # Authentication
    path('login/', MyTokenObtainPairView.as_view(), name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_perfil'),
]

# Add catch-all route for SPA if frontend build exists
if settings.FRONTEND_DIST_EXISTS:
    urlpatterns += [
        # Serve assets directly
        re_path(r'^assets/(?P<path>.*)$', serve, {
            'document_root': str(settings.FRONTEND_DIST / 'assets'),
        }),
        # Catch-all for SPA
        # Exclude api/ paths to allow CommonMiddleware to handle APPEND_SLASH redirects
        re_path(r'^(?!api/).*$', TemplateView.as_view(template_name='index.html'), name='spa'),
    ]
