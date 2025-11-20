# ApiCoreScouts/Permissions.py
from rest_framework.permissions import BasePermission

from .Models.usuario_model import Perfil_Aplicacion

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

        app_name = getattr(view, 'APP_NAME', None)
        perfil = getattr(request.user, 'PEL_ID', None)
        if not perfil:
            return False

        if not app_name:
            return True

        try:
            perfil_aplicacion = perfil.perfil_aplicacion_set.select_related('APL_ID').get(
                APL_ID__APL_DESCRIPCION=app_name
            )
        except Perfil_Aplicacion.DoesNotExist:
            return False

        required_permissions = getattr(view, 'REQUIRED_PERMISSIONS', None)
        if required_permissions is None:
            action_permissions = getattr(view, 'ACTION_PERMISSIONS', {})
            action = getattr(view, 'action', None)
            if action and action_permissions:
                if action not in action_permissions:
                    return False
                required_permissions = action_permissions.get(action)
            else:
                required_permissions = None

        if not required_permissions:
            required_permissions = ('PEA_INGRESAR',)

        if isinstance(required_permissions, str):
            required_permissions = (required_permissions,)

        for perm_name in required_permissions:
            if not hasattr(perfil_aplicacion, perm_name):
                return False
            if not getattr(perfil_aplicacion, perm_name):
                return False

        return True
