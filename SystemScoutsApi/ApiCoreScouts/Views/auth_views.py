from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from ..Models.ModuloUsuarios import Usuario
from ..Models.ModuloPersonas import Persona
from ..Models.ModuloPersonas import Persona_Curso
from ..Models.ModuloCursos import Curso_Seccion, Curso

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


@csrf_exempt
@api_view(["POST"])
def acreditacion_manual_search(request):
	"""
	Busca una persona por RUT (PER_RUN + PER_DV) o por nombre y retorna datos básicos
	junto con el curso actual (si existe) y el estado de acreditación.

	Request JSON: { term: string }
	Response 200: {
	  found: bool,
	  persona: { per_id, nombre, rut },
	  curso: { cur_id, descripcion } | null,
	  acreditado: bool,
	  paymentStatus: string
	}
	"""
	data = request.data or {}
	term = (data.get("term") or "").strip()
	if not term:
		return Response({"detail": "term requerido"}, status=400)

	# Normalizar posible RUT: quitar puntos/guiones
	norm = term.replace(".", "").replace("-", "").upper()

	persona = None
	if norm.isalnum():
		# intentar por PER_RUN + PER_DV
		run = norm[:-1]
		dv = norm[-1:]
		persona = Persona.objects.filter(PER_RUN=run, PER_DV=dv).first()

	if not persona:
		# fallback por nombre contiene
		persona = (
			Persona.objects.filter(PER_NOMBRES__icontains=term)
			.order_by("PER_APELPTA", "PER_NOMBRES")
			.first()
		)

	if not persona:
		return Response({"found": False})

	# Buscar la relación Persona_Curso más reciente
	pec = Persona_Curso.objects.filter(PER_ID=persona).order_by("-PEC_ID").first()
	curso_info = None
	acreditado = False
	if pec:
		# Obtener curso via Curso_Seccion -> Curso
		try:
			cus: Curso_Seccion = pec.CUS_ID
			cur: Curso = cus.CUR_ID
			curso_info = {
				"cur_id": cur.CUR_ID,
				"descripcion": cur.CUR_DESCRIPCION,
				"codigo": cur.CUR_CODIGO,
			}
		except Exception:
			curso_info = None
		acreditado = bool(getattr(pec, "PEC_ACREDITACION", False))

	# Por ahora, como pagos no está enlazado, reportamos "Confirmado" para permitir acreditar manualmente
	payment_status = "Confirmado"

	return Response({
		"found": True,
		"persona": {
			"per_id": persona.PER_ID,
			"nombre": f"{persona.PER_NOMBRES} {persona.PER_APELPTA or ''} {persona.PER_APELMAT or ''}".strip(),
			"rut": f"{persona.PER_RUN}-{persona.PER_DV}",
		},
		"curso": curso_info,
		"acreditado": acreditado,
		"paymentStatus": payment_status,
	})


@csrf_exempt
@api_view(["POST"])
def acreditacion_manual_acreditar(request):
	"""
	Marca la acreditación de una persona en su relación Persona_Curso más reciente.

	Request JSON: { rut: string } | { per_id: number }
	Response 200: { ok: true, acreditado: bool }
	"""
	data = request.data or {}
	per_id = data.get("per_id")
	rut = (data.get("rut") or "").strip()

	persona = None
	if per_id:
		persona = Persona.objects.filter(PER_ID=per_id).first()
	elif rut:
		norm = rut.replace(".", "").replace("-", "").upper()
		if len(norm) >= 2:
			run = norm[:-1]
			dv = norm[-1:]
			persona = Persona.objects.filter(PER_RUN=run, PER_DV=dv).first()

	if not persona:
		return Response({"detail": "Persona no encontrada"}, status=404)

	pec = Persona_Curso.objects.filter(PER_ID=persona).order_by("-PEC_ID").first()
	if not pec:
		return Response({"detail": "Persona no tiene inscripción de curso"}, status=400)

	if not getattr(pec, "PEC_ACREDITACION", False):
		setattr(pec, "PEC_ACREDITACION", True)
		pec.save(update_fields=["PEC_ACREDITACION"])

	return Response({"ok": True, "acreditado": True})