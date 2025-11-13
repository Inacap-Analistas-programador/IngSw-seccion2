from rest_framework import viewsets
from ..Serializers import Archivo_serializer as MA_S
from ..Models.archivo_model import *

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = MA_S.ArchivoSerializer

class ArchivoCursoViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Curso.objects.all()
    serializer_class = MA_S.ArchivoCursoSerializer

class ArchivoPersonaViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Persona.objects.all()
    serializer_class = MA_S.ArchivoPersonaSerializer