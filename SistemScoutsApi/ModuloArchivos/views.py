from rest_framework import viewsets
from ApiCore.serializers import ModuloArchivosSerializers
from .models import (Archivo, Archivo_Curso, Archivo_Persona, Tipo_Archivo)

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = ModuloArchivosSerializers.ArchivoSerializer

class ArchivoCursoViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Curso.objects.all()
    serializer_class = ModuloArchivosSerializers.ArchivoCursoSerializer

class ArchivoPersonaViewSet(viewsets.ModelViewSet):
    queryset = Archivo_Persona.objects.all()
    serializer_class = ModuloArchivosSerializers.ArchivoPersonaSerializer

class TipoArchivoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Archivo.objects.all()
    serializer_class = ModuloArchivosSerializers.TipoArchivoSerializer