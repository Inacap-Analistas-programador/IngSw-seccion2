from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('admin-drf/')),
    path('admin-drf/', admin.site.urls),
<<<<<<< HEAD
    path('api/', include('ApiScouts.urls')),
=======

    path('api/usuarios/', include('ModuloUsuarios.urls')),
    path('api/cursos/', include('ModuloCursos.urls')),
    path('api/pagos/', include('ModuloPagos.urls')),
    path('api/archivos/', include('ModuloArchivos.urls')),
    path('api/mantenedores/', include('ModuloMantenedores.urls')),

    # ruta dinámica global
    path('api/core/', include('ApiCore.urls')),
>>>>>>> fe3ca806e3592a744d4e2b2f7b27c752cbbeef0d
]
