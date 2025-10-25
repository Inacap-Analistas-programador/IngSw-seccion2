from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from ApiCoreScouts.jwt_utils import generar_token
from ApiCoreScouts.decorators import token_requerido
from ..Models.ModuloUsuarios import Usuario

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