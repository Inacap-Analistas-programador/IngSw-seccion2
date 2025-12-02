from django.contrib.auth.backends import BaseBackend
from .Models.usuario_model import *

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
            
            # 1. Verificar hash estándar de Django
            if user.check_password(password):
                if user.is_active:
                    return user
            
            # 2. Respaldo: Verificar contraseña en texto plano (para datos importados heredados)
            # Si coincide, actualizar al hash automáticamente
            elif user.password == password:
                if user.is_active:
                    user.set_password(password)
                    user.save()
                    return user
                    
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
