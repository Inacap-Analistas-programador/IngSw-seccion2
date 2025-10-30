from rest_framework import viewsets
from ..Serializers import Personas_serializers as MU_S
from ..Models.ModuloPersonas import *

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = MU_S.PersonaSerializer

class PersonaCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Curso.objects.all()
    serializer_class = MU_S.PersonaCursoSerializer

class PersonaGrupoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Grupo.objects.all()
    serializer_class = MU_S.PersonaGrupoSerializer

class PersonaFormadorViewSet(viewsets.ModelViewSet):
    queryset = Persona_Formador.objects.all()
    serializer_class = MU_S.PersonaFormadorSerializer

class PersonaIndividualViewSet(viewsets.ModelViewSet):
    queryset = Persona_Individual.objects.all()
    serializer_class = MU_S.PersonaIndividualSerializer

class PersonaNivelViewSet(viewsets.ModelViewSet):
    queryset = Persona_Nivel.objects.all()
    serializer_class = MU_S.PersonaNivelSerializer

class PersonaCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Curso.objects.all()
    serializer_class = MU_S.PersonaCursoSerializer

class PersonaEstadoCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Estado_Curso.objects.all()
    serializer_class = MU_S.PersonaEstadoCursoSerializer

class PersonaVehiculoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Vehiculo.objects.all()
    serializer_class = MU_S.PersonaVehiculoSerializer