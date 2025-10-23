from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.apps import apps
from ApiCore.serializers import serializers_dict
from ApiCore.decorators import token_requerido, permiso_requerido


@api_view(['POST'])
def login_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'success': True, 'token': token})
    else:
        return Response({'success': False}, status=401)
    
class DynamicModelViewSet(viewsets.ModelViewSet):
    """
    Vista dinámica que gestiona cualquier modelo del proyecto.
    Protegida con JWT y control de permisos por rol.
    """

    def get_serializer_class(self):
        model_name = self.kwargs['model_name']
        return serializers_dict.get(model_name)

    def get_queryset(self):
        app_name = self.kwargs['app_name']
        model_name = self.kwargs['model_name']
        model = apps.get_model(app_name, model_name)
        return model.objects.all()

    # ----------------------------
    # Protecciones por acción
    # ----------------------------


    @token_requerido
    @permiso_requerido(nombre_aplicacion="ApiCore", accion="consultar")
    def list(self, request, *args, **kwargs):
        """Listar registros"""
        return super().list(request, *args, **kwargs)

    @token_requerido
    @permiso_requerido(nombre_aplicacion="ApiCore", accion="ingresar")
    def create(self, request, *args, **kwargs):
        """Crear registro"""
        return super().create(request, *args, **kwargs)

    @token_requerido
    @permiso_requerido(nombre_aplicacion="ApiCore", accion="modificar")
    def update(self, request, *args, **kwargs):
        """Actualizar registro"""
        return super().update(request, *args, **kwargs)

    @token_requerido
    @permiso_requerido(nombre_aplicacion="ApiCore", accion="eliminar")
    def destroy(self, request, *args, **kwargs):
        """Eliminar registro"""
        return super().destroy(request, *args, **kwargs)
