# ApiCoreScouts/Permissions.py
from rest_framework.permissions import BasePermission

from .Models.usuario_model import Perfil_Aplicacion

class PerfilPermission(BasePermission):
    """
    Permite acceso según el perfil y la aplicación.
    Se puede extender para revisar pea_ingresar, modificar, etc.
    """
    def has_permission(self, request, view):
        # Debe estar autenticado
        if not request.user.is_authenticated:
            return False

        # Debe estar vigente
        if not getattr(request.user, 'usu_vigente', False):
            return False

        # Bypass: si es superuser (usu_is_superuser True) permitir todo sin revisar flags.
        # Se mantiene estricto para otros usuarios (staff no bypass).
        if getattr(request.user, 'is_superuser', False):
            return True

        perfil = getattr(request.user, 'pel_id', None)
        if not perfil:
            return False

        app_name = getattr(view, 'app_name', None)
        # Si la vista no tiene APP_NAME, permitir (solo valida autenticación básica)
        if not app_name:
            return True

        try:
            perfil_aplicacion = perfil.perfil_aplicacion_set.select_related('apl_id').get(
                apl_id__apl_descripcion=app_name
            )
        except Perfil_Aplicacion.DoesNotExist:
            # Debug: no existe relación perfil-aplicación
            try:
                print(f"[PerfilPermission] Perfil_Aplicacion missing for perfil={perfil.pel_id} app={app_name}")
            except Exception:
                pass
            return False

        # Determinar permisos requeridos según acción o método HTTP
        required_permissions = getattr(view, 'REQUIRED_PERMISSIONS', None)
        if required_permissions is None:
            action_permissions = getattr(view, 'ACTION_PERMISSIONS', {})
            action = getattr(view, 'action', None)
            if action and action_permissions:
                # Si la acción no está mapeada, denegar explícitamente
                if action not in action_permissions:
                    try:
                        print(f"[PerfilPermission] action '{action}' not mapped in ACTION_PERMISSIONS for app={app_name}")
                    except Exception:
                        pass
                    return False
                required_permissions = action_permissions.get(action)
            else:
                # Fallback por método: métodos de sólo lectura usan CONSULTAR
                if request.method in ('GET', 'HEAD', 'OPTIONS'):
                    required_permissions = ('pea_consultar',)
                elif request.method == 'POST':
                    required_permissions = ('pea_ingresar',)
                elif request.method in ('PUT', 'PATCH'):
                    required_permissions = ('pea_modificar',)
                elif request.method == 'DELETE':
                    required_permissions = ('pea_eliminar',)
                else:
                    # Método desconocido: denegar
                    return False

        # Normalizar a tupla
        if isinstance(required_permissions, str):
            required_permissions = (required_permissions,)

        # Validar flags en Perfil_Aplicacion
        for perm_name in required_permissions:
            if not hasattr(perfil_aplicacion, perm_name):
                try: print(f"[PerfilPermission] perm flag '{perm_name}' missing on Perfil_Aplicacion id={getattr(perfil_aplicacion,'pea_id',None)}")
                except Exception: pass
                return False
            if not getattr(perfil_aplicacion, perm_name):
                try: print(f"[PerfilPermission] perm flag '{perm_name}'=False for perfil_aplicacion id={getattr(perfil_aplicacion,'pea_id',None)}")
                except Exception: pass
                return False

        return True
