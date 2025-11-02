from django.urls import path
from .views import login, perfil

urlpatterns = [
    path('login/', login, name='auth_login'),
    path('perfil/', perfil, name='auth_perfil'),
]
