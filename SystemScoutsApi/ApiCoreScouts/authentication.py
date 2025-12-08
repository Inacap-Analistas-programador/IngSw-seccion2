from django.contrib.auth.backends import BaseBackend
from .Models.usuario_model import *
import logging

logger = logging.getLogger(__name__)

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Si se usa un campo de usuario personalizado (usu_username), puede venir en kwargs
        if username is None:
            username = kwargs.get('usu_username')

        if username is None or password is None:
            return None
        try:
            # Usar iexact para búsqueda de nombre de usuario insensible a mayúsculas/minúsculas
            user = Usuario.objects.get(usu_username__iexact=username)
            
            # Verificar hash estándar de Django
            if user.check_password(password):
                if user.is_active:
                    return user
            else:
                # Log failed authentication attempt without exposing password
                logger.warning(f"Failed authentication attempt for user: {username}")
                return None
                    
        except Usuario.DoesNotExist:
            logger.warning(f"Authentication attempt for non-existent user: {username}")
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
