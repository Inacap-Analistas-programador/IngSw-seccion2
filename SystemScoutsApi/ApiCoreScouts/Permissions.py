# ApiCoreScouts/Permissions.py
from rest_framework.permissions import BasePermission

class PerfilPermission(BasePermission):
    """
    Permite acceso según los permisos nativos de Django.
    Mapea las acciones y app_name a codenames de permisos.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.is_active:
            return False

        if request.user.is_superuser:
            return True

        if not hasattr(view, 'queryset') or view.queryset is None:
            return True

        model = view.queryset.model
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        
        # Determine standard Django action
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            action = 'view'
        elif request.method == 'POST':
            action = 'add'
        elif request.method in ('PUT', 'PATCH'):
            action = 'change'
        elif request.method == 'DELETE':
            action = 'delete'
        else:
            return False

        perm_codename = f"{app_label}.{action}_{model_name}"
        
        # Check permission
        return request.user.has_perm(perm_codename)

