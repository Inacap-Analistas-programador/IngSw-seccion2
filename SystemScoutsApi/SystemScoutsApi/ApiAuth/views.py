from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from ApiCoreScouts.Models.ModuloUsuarios import Usuario
from SystemScoutsApi.ApiAuth.jwt_utils import generar_token
from SystemScoutsApi.ApiAuth.decorators import token_requerido

@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "Faltan credenciales"}, status=400)

    try:
        usuario = Usuario.objects.get(USU_USERNAME=username)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)

    if usuario.USU_PASSWORD != password:  
        return Response({"error": "Credenciales inválidas"}, status=401)

    token = generar_token(usuario)
    return Response({
        "token": token,
        "usuario": {"id": usuario.USU_ID, "username": usuario.USU_USERNAME}
    })

@api_view(['GET'])
@token_requerido
def perfil(request):
    return Response({
        "mensaje": "OK",
        "usuario": request.user_data
    })
