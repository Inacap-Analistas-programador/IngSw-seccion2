# ModuloUsuarios/views.py
from rest_framework import viewsets
from ApiCore.serializers import ModuloUsuariosSerializers
from ModuloUsuarios.models import Usuario

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = ModuloUsuariosSerializers.UsuarioSerializer
