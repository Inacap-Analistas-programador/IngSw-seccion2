from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from ..Models.ModuloUsuarios import Usuario
from ..Models.ModuloPersonas import Persona

import secrets


@csrf_exempt
@api_view(["POST"])
def login(request):
	"""
	Login mínimo (no seguro para producción): valida USU_USERNAME y USU_PASSWORD
	contra la tabla Usuario y retorna un token de sesión simple.

	Request JSON: { "username": string, "password": string }
	Response 200: { "token": string, "user": { ...campos básicos } }
	Response 401: { "detail": "Credenciales inválidas" }
	"""
	data = request.data or {}
	username = data.get("username")
	password = data.get("password")

	if not username or not password:
		return Response({"detail": "username y password son requeridos"}, status=400)

	user = (
		Usuario.objects.filter(USU_USERNAME=username, USU_PASSWORD=password, USU_VIGENTE=True)
		.first()
	)
	if not user:
		return Response({"detail": "Credenciales inválidas"}, status=401)

	# Genera un token aleatorio (placeholder). En producción usar JWT/djangorestframework-simplejwt
	token = secrets.token_urlsafe(32)

	user_payload = {
		"USU_ID": user.USU_ID,
		"USU_USERNAME": user.USU_USERNAME,
		"PEL_ID": getattr(user, "PEL_ID_id", None),
		"USU_RUTA_FOTO": getattr(user, "USU_RUTA_FOTO", None),
		"USU_VIGENTE": getattr(user, "USU_VIGENTE", True),
	}
	return Response({"token": token, "user": user_payload})


@csrf_exempt
@api_view(["POST"])
def qr_token(request):
	"""
	Genera un token QR firmado de corta duración (placeholder).
	Request JSON: { ids: [int], tipo: str, expSeconds: int, usuId: int }
	Response: { token: str }
	"""
	data = request.data or {}
	ids = data.get("ids") or []
	tipo = data.get("tipo") or "generic"
	exp = int(data.get("expSeconds") or 3600)

	# Token simple: tipo|timestamp|aleatorio|nIds
	now_ts = int(timezone.now().timestamp())
	token = f"QR|{tipo}|{now_ts}|{secrets.token_urlsafe(16)}|{len(ids)}|exp={exp}"
	return Response({"token": token})


@csrf_exempt
@api_view(["POST"])
def qr_email(request):
	"""
	Simula envío de correos para los IDs de personas recibidos y retorna conteos.
	Request JSON: { ids: [int], tipo: str, expSeconds: int, usuId: int }
	Response: { solicitados: int, procesados: int, enviados: int }
	"""
	data = request.data or {}
	ids = data.get("ids") or []

	personas = list(Persona.objects.filter(PER_ID__in=ids))
	procesados = 0
	enviados = 0
	for p in personas:
		email = getattr(p, "PER_MAIL", None)
		vigente = bool(getattr(p, "PER_VIGENTE", True))
		if vigente and email:
			procesados += 1
			enviados += 1
			# Simulación: imprimir en consola del servidor
			print(f"[QR EMAIL] Enviado a {email} (PER_ID={p.PER_ID})")

	return Response({
		"solicitados": len(ids),
		"procesados": procesados,
		"enviados": enviados,
	})