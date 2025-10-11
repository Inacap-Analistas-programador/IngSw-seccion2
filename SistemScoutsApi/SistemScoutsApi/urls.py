from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('admin-drf/')),
    path('admin-drf/', admin.site.urls),
    path('api/', include('ApiScouts.urls')),
]
