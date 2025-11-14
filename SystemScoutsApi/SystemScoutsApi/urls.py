from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


from ApiCoreScouts.Routers.Usuario_router import router as usuario_router
from ApiCoreScouts.Routers.Curso_router import router as curso_router
from ApiCoreScouts.Routers.Archivo_router import router as archivo_router
from ApiCoreScouts.Routers.Pago_router import router as pago_router
from ApiCoreScouts.Routers.Mantenedor_router import router as mantenedor_router
from ApiCoreScouts.Routers.Persona_router import router as personas_router

from rest_framework_simplejwt.views import TokenRefreshView
from ApiCoreScouts.Views.Usuario_view import MyTokenObtainPairView

urlpatterns = [
    path('api/usuarios/', include(usuario_router.urls)),
    path('api/personas/', include(personas_router.urls)),
    path('api/cursos/', include(curso_router.urls)),
    path('api/archivos/', include(archivo_router.urls)),
    path('api/mantenedores/', include(mantenedor_router.urls)),
    path('api/pagos/', include(pago_router.urls)),
    #Authentication
    path('login/', MyTokenObtainPairView.as_view(), name='auth_login'), 
    path('refresh/', TokenRefreshView.as_view(), name='auth_perfil'),
]
