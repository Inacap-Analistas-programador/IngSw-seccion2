# ModuloUsuarios/views.py
from rest_framework import viewsets
from ApiCore.serializers import ModuloUsuariosSerializers
from .models import (Usuario, Perfil, Aplicacion, Persona, Persona_Grupo, Persona_Formador, Persona_Individual, Persona_Nivel, Persona_Curso, Persona_Estado_Curso, Persona_Vehiculo, Perfil_Aplicacion)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = ModuloUsuariosSerializers.UsuarioSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = ModuloUsuariosSerializers.PersonaSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = ModuloUsuariosSerializers.PerfilSerializer

class AplicacionViewSet(viewsets.ModelViewSet):
    queryset = Aplicacion.objects.all()
    serializer_class = ModuloUsuariosSerializers.AplicacionSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona_Curso.objects.all()
    serializer_class = ModuloUsuariosSerializers.PersonaSerializer

class PersonaGrupoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Grupo.objects.all()
    serializer_class = ModuloUsuariosSerializers.PersonaGrupoSerializer

class PersonaFormadorViewSet(viewsets.ModelViewSet):
    queryset = Persona_Formador.objects.all()
    serializer_class = ModuloUsuariosSerializers.PersonaFormadorSerializer

class PersonaIndividualViewSet(viewsets.ModelViewSet):
    queryset = Persona_Individual.objects.all()
    serializer_class = ModuloUsuariosSerializers.PersonaIndividualSerializer

class PersonaNivelViewSet(viewsets.ModelViewSet):
    queryset = Persona_Nivel.objects.all()
    serializer_class = ModuloUsuariosSerializers.PersonaNivelSerializer

class PersonaCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Curso.objects.all()
    serializer_class = ModuloUsuariosSerializers.PersonaCursoSerializer

class PersonaEstadoCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Estado_Curso.objects.all()
    serializer_class = ModuloUsuariosSerializers.PersonaEstadoCursoSerializer

class PersonaVehiculoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Vehiculo.objects.all()
    serializer_class = ModuloUsuariosSerializers.PersonaVehiculoSerializer

class PerfilAplicacionViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Aplicacion.objects.all()
    serializer_class = ModuloUsuariosSerializers.perfilAplicacionSerializer

