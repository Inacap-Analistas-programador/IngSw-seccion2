from rest_framework import viewsets
from ..Serializers import Persona_serializer as MU_S
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from ..Filters.persona_filter import *
from ..Models.persona_model import *

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = MU_S.PersonaSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonaFilter
    renderer_classes = [JSONRenderer]

class PersonaCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Curso.objects.all()
    serializer_class = MU_S.PersonaCursoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonaCursoFilter
    renderer_classes = [JSONRenderer]

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

class PersonaEstadoCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Estado_Curso.objects.all()
    serializer_class = MU_S.PersonaEstadoCursoSerializer

class PersonaVehiculoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Vehiculo.objects.all()
    serializer_class = MU_S.PersonaVehiculoSerializer