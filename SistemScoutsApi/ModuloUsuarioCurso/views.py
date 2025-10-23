from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from ApiCore.jwt_utils import generar_token
from ApiCore.decorators import token_requerido
from ApiCore.serializers import ModuloUsuarioCursoSerializers
from .models import (Usuario, Perfil, Aplicacion, Persona, Persona_Grupo, Persona_Formador, Persona_Individual, Persona_Nivel, Persona_Curso, Persona_Estado_Curso, Persona_Vehiculo, Perfil_Aplicacion)
from .models import (Curso, Curso_Cuota, Curso_Fecha, Curso_Alimentacion, Curso_Coordinador, Curso_Seccion, Curso_Formador, Tipo_Curso)

# ======================================================
# VIEWSET GENERAL (CRUD)
# ======================================================
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    CRUD básico para la gestión de usuarios.
    """
    queryset = Usuario.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.UsuarioSerializer


# ======================================================
# LOGIN CON JWT
# ======================================================
@csrf_exempt
@api_view(['POST'])
def login(request):
    """
    Autentica a un usuario y devuelve un token JWT.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    # Validar que los campos existan
    if not username or not password:
        return Response({"error": "Faltan credenciales"}, status=400)

    # Buscar usuario en la base de datos
    try:
        usuario = Usuario.objects.get(USU_USERNAME=username)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)

    # Verificar contraseña (actualmente texto plano)
    if usuario.USU_PASSWORD != password:
        return Response({"error": "Contraseña incorrecta"}, status=401)

    # Generar token JWT
    token = generar_token(usuario)
    return Response({
        "token": token,
        "usuario": {
            "id": usuario.USU_ID,
            "username": usuario.USU_USERNAME
        }
    })


# ======================================================
# RUTA PROTEGIDA (EJEMPLO)
# ======================================================
@api_view(['GET'])
@token_requerido
def perfil_usuario(request):
    """
    Devuelve los datos del usuario autenticado.
    Requiere un token JWT válido en la cabecera.
    """
    user_data = request.user_data
    return Response({
        "mensaje": "Acceso permitido",
        "usuario": user_data
    })


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.CursoSerializer

class CursoCuotaViewSet(viewsets.ModelViewSet):
    queryset = Curso_Cuota.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.CursoCuotaSerializer

class CursoFechaViewSet(viewsets.ModelViewSet):
    queryset = Curso_Fecha.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.CursoFechaSerializer

class CursoAlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Alimentacion.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.CursoAlimentacionSerializer

class CursoCoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Coordinador.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.CursoCoordinadorSerializer

class CursoSeccionViewSet(viewsets.ModelViewSet):
    queryset = Curso_Seccion.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.CursoSeccionSerializer

class CursoFormadorViewSet(viewsets.ModelViewSet):
    queryset = Curso_Formador.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.CursoFormadorSerializer

class TipoCursoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Curso.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.TipoCursoSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.UsuarioSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PersonaSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PerfilSerializer

class AplicacionViewSet(viewsets.ModelViewSet):
    queryset = Aplicacion.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.AplicacionSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona_Curso.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PersonaSerializer

class PersonaGrupoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Grupo.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PersonaGrupoSerializer

class PersonaFormadorViewSet(viewsets.ModelViewSet):
    queryset = Persona_Formador.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PersonaFormadorSerializer

class PersonaIndividualViewSet(viewsets.ModelViewSet):
    queryset = Persona_Individual.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PersonaIndividualSerializer

class PersonaNivelViewSet(viewsets.ModelViewSet):
    queryset = Persona_Nivel.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PersonaNivelSerializer

class PersonaCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Curso.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PersonaCursoSerializer

class PersonaEstadoCursoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Estado_Curso.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PersonaEstadoCursoSerializer

class PersonaVehiculoViewSet(viewsets.ModelViewSet):
    queryset = Persona_Vehiculo.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PersonaVehiculoSerializer

class PerfilAplicacionViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Aplicacion.objects.all()
    serializer_class = ModuloUsuarioCursoSerializers.PerfilAplicacionSerializer

