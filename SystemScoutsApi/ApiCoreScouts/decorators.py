from functools import wraps
from django.http import JsonResponse
from .jwt_utils import validar_token
from .Models.ModuloUsuarios import Usuario, Perfil_Aplicacion, Aplicacion

def _get_token_from_header(request):
    """Extrae y valida el formato del token JWT en la cabecera Authorization."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None, JsonResponse({"error": "Token no proporcionado"}, status=401)
    try:
        scheme, token = auth_header.split(" ", 1)
        if scheme.lower() != "bearer":
            return None, JsonResponse({"error": "Usa 'Bearer <token>'"}, status=401)
        return token, None
    except ValueError:
        return None, JsonResponse({"error": "Formato de token inválido"}, status=401)


def token_requerido(view_func):
    """Valida que el request incluya un token JWT válido."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token, err = _get_token_from_header(request)
        if err:
            return err

        payload = validar_token(token)
        if not payload:
            return JsonResponse({"error": "Token inválido o expirado"}, status=401)

        # Guarda los datos del usuario en la request
        request.user_data = payload
        return view_func(request, *args, **kwargs)
    return wrapper


def permiso_requerido(nombre_aplicacion: str, accion: str):
    """
    Verifica si el usuario tiene permiso para ejecutar una acción específica en una aplicación.
    
    nombre_aplicacion: debe coincidir con Aplicacion.APL_DESCRIPCION (ej. 'ModuloUsuarios')
    accion: 'consultar' | 'ingresar' | 'modificar' | 'eliminar'
    """
    accion = accion.lower()
    validas = {"consultar", "ingresar", "modificar", "eliminar"}
    if accion not in validas:
        raise ValueError(f"Acción inválida: {accion}")

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            token, err = _get_token_from_header(request)
            if err:
                return err

            payload = validar_token(token)
            if not payload:
                return JsonResponse({"error": "Token inválido o expirado"}, status=401)

            # Obtener el usuario
            user_id = payload.get("user_id")
            try:
                usuario = Usuario.objects.select_related("PEL_ID").get(USU_ID=user_id)
            except Usuario.DoesNotExist:
                return JsonResponse({"error": "Usuario del token no existe"}, status=401)

            # Verificar permisos del perfil sobre la aplicación
            try:
                app = Aplicacion.objects.get(APL_DESCRIPCION=nombre_aplicacion, APL_VIGENTE=True)
                pea = Perfil_Aplicacion.objects.get(PEL_ID=usuario.PEL_ID, APL_ID=app)
            except (Aplicacion.DoesNotExist, Perfil_Aplicacion.DoesNotExist):
                return JsonResponse({"error": "No tienes permisos para esta aplicación"}, status=403)

            # Validar acción
            permisos = {
                "consultar": pea.PEA_CONSULTAR,
                "ingresar": pea.PEA_INGRESAR,
                "modificar": pea.PEA_MODIFICAR,
                "eliminar": pea.PEA_ELIMINAR,
            }

            if not permisos.get(accion, False):
                return JsonResponse({"error": f"No tienes permiso para {accion}"}, status=403)

            # Guardar info del usuario para la vista
            request.user_data = payload
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
