from rest_framework import viewsets
from ..Serializers import Usuarios_serializers as MU_S
from ..Models.ModuloUsuarios import *

# ======================================================
# VIEWSETS USUARIOS Y PERFILES
# ======================================================
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = MU_S.UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = MU_S.UsuarioSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = MU_S.PersonaSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = MU_S.PerfilSerializer

class AplicacionViewSet(viewsets.ModelViewSet):
    queryset = Aplicacion.objects.all()
    serializer_class = MU_S.AplicacionSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona_Curso.objects.all()
    serializer_class = MU_S.PersonaSerializer

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

class PerfilAplicacionViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Aplicacion.objects.all()
    serializer_class = MU_S.PerfilAplicacionSerializer


