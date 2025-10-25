from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView,)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from ApiCoreScouts.Api_Views.Authentication_view import CustomTokenObtainPairSerializer


from ApiCoreScouts.Routers.Usuarios_router import router as usuario_router
from ApiCoreScouts.Routers.Cursos_router import router as curso_router
from ApiCoreScouts.Routers.Archivos_router import router as archivo_router
from ApiCoreScouts.Routers.Pagos_router import router as pago_router
from ApiCoreScouts.Routers.Mantenedores_router import router as mantenedor_router
from ApiCoreScouts.Routers.Personas_router import router as personas_router

urlpatterns = [
    path('', lambda request: redirect('admin-drf/')),
    path('admin-drf/', admin.site.urls),


    path('api/token/', CustomTokenObtainPairSerializer.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='auth_verify'),

    path('api/usuarios/', include(usuario_router.urls)),
    path('api/personas/', include(personas_router.urls)),
    path('api/cursos/', include(curso_router.urls)),
    path('api/archivos/', include(archivo_router.urls)),
    path('api/mantenedores/', include(mantenedor_router.urls)),
    path('api/pagos/', include(pago_router.urls)),
]
