from rest_framework import viewsets
from ..Serializers import Archivos_serializers as MA_S
from ..Models.ModuloArchivos import *

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = MA_S.ArchivoSerializer

class ArchivoCursoViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Curso.objects.all()
    serializer_class = MA_S.ArchivoCursoSerializer

class ArchivoPersonaViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Persona.objects.all()
    serializer_class = MA_S.ArchivoPersonaSerializer