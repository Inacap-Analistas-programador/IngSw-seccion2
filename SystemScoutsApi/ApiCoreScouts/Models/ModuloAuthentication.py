from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .ModuloUsuarios import Usuario

class UsuarioScoutAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            usuario = Usuario.objects.get(USU_USERNAME=username, USU_VIGENTE=True)
            if check_password(password, usuario.USU_PASSWORD):
                return usuario
        except Usuario.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return Usuario.objects.get(USU_ID=user_id, USU_VIGENTE=True)
        except Usuario.DoesNotExist:
            return None