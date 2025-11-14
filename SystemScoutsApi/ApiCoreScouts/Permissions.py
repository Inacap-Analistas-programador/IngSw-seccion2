# ApiCoreScouts/Permissions.py
from rest_framework.permissions import BasePermission

class PerfilPermission(BasePermission):
    """
    Permite acceso según el perfil y la aplicación.
    Se puede extender para revisar PEA_INGRESAR, MODIFICAR, etc.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Ejemplo: solo usuarios activos
        if not request.user.USU_VIGENTE:
            return False

        # Ejemplo: chequea si el usuario tiene permiso de ingresar a una app específica
        app_name = getattr(view, 'APP_NAME', None)
        if app_name:
            return request.user.PEL_ID.perfil_aplicacion_set.filter(APL_ID__APL_DESCRIPCION=app_name, PEA_INGRESAR=True).exists()
        
        return True
