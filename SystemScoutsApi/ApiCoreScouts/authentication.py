from django.contrib.auth.backends import BaseBackend
from .Models.usuario_model import *

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            user = Usuario.objects.get(USU_USERNAME=username)
            if user.check_password(password) and user.is_active:
                return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
