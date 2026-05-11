from rest_framework import viewsets
from ..Serializers import Archivo_serializer as MA_S
from ..Models.archivo_model import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
import os
import uuid
from ..Permissions import PerfilPermission

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = MA_S.ArchivoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Archivos"
    ACTION_PERMISSIONS = {
        'list': ('pea_consultar',),
        'retrieve': ('pea_consultar',),
        'create': ('pea_ingresar',),
        'update': ('pea_modificar',),
        'partial_update': ('pea_modificar',),
        'destroy': ('pea_eliminar',),
        'upload': (), # Accessible if permit allows or handled via permissions
    }

    @action(detail=False, methods=['post'], permission_classes=[])
    def upload(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No se proporcionó ningún archivo'}, status=400)
        
        # Create 'archivos' directory if it doesn't exist (handled by default_storage mostly)
        ext = os.path.splitext(file_obj.name)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"
        
        # Save file to MEDIA_ROOT/archivos
        path = default_storage.save(os.path.join('archivos', unique_filename), file_obj)
        
        # Get tar_id from request or default to 1 (Foto Perfil)
        tar_id = request.data.get('tar_id', 1)
        
        # Create DB record
        try:
            archivo = Archivo.objects.create(
                arc_descripcion=file_obj.name,
                arc_ruta=path,
                tar_id_id=tar_id,
                usu_id_crea_id=request.user.id if request.user.is_authenticated else 1,
                arc_vigente=True
            )
        except Exception as e:
            # Clean up file if DB record creation fails
            if default_storage.exists(path):
                default_storage.delete(path)
            return Response({'error': f'Error al crear registro de archivo: {str(e)}'}, status=500)
        
        serializer = MA_S.ArchivoSerializer(archivo)
        return Response(serializer.data, status=201)

class ArchivoCursoViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Curso.objects.all()
    serializer_class = MA_S.ArchivoCursoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Archivos"
    ACTION_PERMISSIONS = ArchivoViewSet.ACTION_PERMISSIONS

class ArchivoPersonaViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Persona.objects.all()
    serializer_class = MA_S.ArchivoPersonaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [PerfilPermission]
    APP_NAME = "Archivos"
    ACTION_PERMISSIONS = ArchivoViewSet.ACTION_PERMISSIONS
