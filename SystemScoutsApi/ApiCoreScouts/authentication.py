
from django.contrib.auth.backends import BaseBackend
from .Models.usuario_model import Usuario
from .Models.security_model import SL

# funcioncita para sacar la ip del cliente
def gip(rq):
    if not rq:
        return None
    xff = rq.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        ip = xff.split(',')[0]
    else:
        ip = rq.META.get('REMOTE_ADDR')
    return ip

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # si viene el username en los kwargs lo sacamos de ahi
        if username is None:
            username = kwargs.get('usu_username')

        if username is None or password is None:
            return None
            
        ip = gip(request)

        try:
            # buscamos al usuario sin importar mayusculas o minusculas
            u = Usuario.objects.get(usu_username__iexact=username)
            
            # revisamos si la password esta bien
            if u.check_password(password):
                if u.is_active:
                    # todo bien, registramos el login exitoso
                    if request:
                        SL.objects.create(
                            us=u,
                            et='LOGIN_SUCCESS',
                            ip=ip,
                            dt=f"Login OK: {username}",
                            ua=request.META.get('HTTP_USER_AGENT', '')[:255]
                        )
                    return u
                else:
                    # el usuario existe pero esta inactivo, que pena
                    if request:
                        SL.objects.create(
                            us=u,
                            et='LOGIN_FAIL',
                            ip=ip,
                            dt=f"User Inactive: {username}",
                            ua=request.META.get('HTTP_USER_AGENT', '')[:255]
                        )
            else:
                # contraseña incorrecta, a la carcel
                if request:
                    SL.objects.create(
                        us=u,
                        et='LOGIN_FAIL',
                        ip=ip,
                        dt=f"Bad Pass: {username}",
                        ua=request.META.get('HTTP_USER_AGENT', '')[:255]
                    )
                    
        except Usuario.DoesNotExist:
            # no existe el usuario, registramos el intento fallido
            if request:
                SL.objects.create(
                    et='LOGIN_FAIL',
                    ip=ip,
                    dt=f"No User: {username}",
                    ua=request.META.get('HTTP_USER_AGENT', '')[:255]
                )
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
