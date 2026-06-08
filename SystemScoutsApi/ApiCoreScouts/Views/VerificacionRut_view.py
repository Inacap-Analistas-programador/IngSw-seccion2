"""
VerificacionRut_view.py
Endpoints públicos (sin autenticación JWT) para:
  1. POST /api/verificar-rut/  → verifica si el RUT existe y envía código al correo
  2. POST /api/verificar-rut/confirmar/ → valida el código y devuelve los datos básicos de la persona
"""
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..Models.persona_model import Persona
import secrets
import logging

logger = logging.getLogger(__name__)

CACHE_PREFIX = 'rut_verify_'
CODE_TTL_SECONDS = 600  # 10 minutos


def _mask_email(email: str) -> str:
    """Oculta parte del correo para mostrar al usuario: j***@gmail.com"""
    if not email or '@' not in email:
        return '***@***.com'
    local, domain = email.split('@', 1)
    masked_local = local[0] + '***' if len(local) > 1 else '***'
    return f'{masked_local}@{domain}'


@api_view(['POST'])
@permission_classes([AllowAny])
def solicitar_codigo_rut(request):
    """
    Paso 1: El usuario ingresa su RUT.
    - Limpia el RUT (solo dígitos, sin dv)
    - Busca la persona en BD
    - Genera un código de 6 dígitos y lo guarda en cache (10 min)
    - Envía el código al correo registrado
    - Devuelve la dirección de correo enmascarada
    """
    rut_raw = request.data.get('rut', '').strip()
    if not rut_raw:
        return Response({'error': 'El RUT es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

    # Limpiar: sacar puntos, guión y dígito verificador
    cleaned = rut_raw.replace('.', '').replace('-', '').upper()
    if len(cleaned) < 2:
        return Response({'error': 'RUT inválido.'}, status=status.HTTP_400_BAD_REQUEST)

    # El run en BD no incluye el DV
    run = cleaned[:-1]

    try:
        persona = Persona.objects.get(per_run=run, per_vigente=True)
    except Persona.DoesNotExist:
        # No revelar si el RUT existe o no (seguridad)
        return Response(
            {'error': 'No se encontró un registro activo para ese RUT.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not persona.per_mail:
        return Response(
            {'error': 'La persona no tiene correo registrado. Contacta a un administrador.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Generar código de 6 dígitos
    code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])

    # Guardar en cache: key = rut_verify_{run} → {'code': ..., 'per_id': ...}
    cache_key = f'{CACHE_PREFIX}{run}'
    cache.set(cache_key, {'code': code, 'per_id': persona.per_id}, CODE_TTL_SECONDS)

    # Enviar correo
    try:
        send_mail(
            subject='Código de verificación - Sistema Scouts',
            message=(
                f'Hola {persona.per_nombres},\n\n'
                f'Tu código de verificación para acceder al formulario de inscripción es:\n\n'
                f'  {code}\n\n'
                f'Este código es válido por 10 minutos. No lo compartas con nadie.\n\n'
                f'Si no solicitaste este código, ignora este mensaje.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[persona.per_mail],
            fail_silently=False,
        )
        logger.info(f'Código de verificación enviado a per_run={run}')
    except Exception as e:
        logger.error(f'Error al enviar correo de verificación para per_run={run}: {e}')
        return Response(
            {'error': 'Error al enviar el correo. Intenta nuevamente.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({
        'ok': True,
        'email_masked': _mask_email(persona.per_mail),
        'message': 'Se envió un código de verificación al correo registrado.'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmar_codigo_rut(request):
    """
    Paso 2: El usuario ingresa el código recibido por correo.
    - Valida el código contra el cache
    - Si es correcto, devuelve los datos básicos de la persona para pre-llenar el formulario
    """
    rut_raw = request.data.get('rut', '').strip()
    codigo = request.data.get('codigo', '').strip()

    if not rut_raw or not codigo:
        return Response(
            {'error': 'RUT y código son obligatorios.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    cleaned = rut_raw.replace('.', '').replace('-', '').upper()
    if len(cleaned) < 2:
        return Response({'error': 'RUT inválido.'}, status=status.HTTP_400_BAD_REQUEST)
    run = cleaned[:-1]

    cache_key = f'{CACHE_PREFIX}{run}'
    cached = cache.get(cache_key)

    if not cached:
        return Response(
            {'error': 'El código ha expirado o no existe. Solicita uno nuevo.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if cached['code'] != codigo:
        return Response(
            {'error': 'Código incorrecto. Verifica e intenta nuevamente.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Código correcto → invalidar cache e ir a buscar datos
    cache.delete(cache_key)

    try:
        persona = Persona.objects.get(per_id=cached['per_id'])
    except Persona.DoesNotExist:
        return Response({'error': 'Persona no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

    # Devolver datos para pre-llenar el formulario
    data = {
        'per_id': persona.per_id,
        'per_run': persona.per_run,
        'per_dv': persona.per_dv,
        'per_nombres': persona.per_nombres,
        'per_apelpta': persona.per_apelpta,
        'per_apelmat': persona.per_apelmat or '',
        'per_mail': persona.per_mail,
        'per_fecha_nac': persona.per_fecha_nac.strftime('%Y-%m-%d') if persona.per_fecha_nac else '',
        'per_direccion': persona.per_direccion or '',
        'per_fono': persona.per_fono or '',
        'per_apodo': persona.per_apodo or '',
        'com_id': persona.com_id_id,
    }

    logger.info(f'Verificación exitosa para per_id={persona.per_id}')
    return Response({'ok': True, 'persona': data})
