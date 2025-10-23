import jwt
from datetime import datetime, timedelta
from django.conf import settings

# Configuración del token JWT
SECRET_KEY = getattr(settings, "SECRET_KEY", "clave_super_secreta")
ALGORITHM = "HS256"
TOKEN_DURATION = timedelta(hours=2)

def generar_token(usuario):
    """
    Genera un token JWT válido por TOKEN_DURATION horas.
    Contiene el ID y nombre de usuario.
    """
    payload = {
        "user_id": usuario.USU_ID,
        "username": usuario.USU_USERNAME,
        "exp": datetime.utcnow() + TOKEN_DURATION,  # Expiración
        "iat": datetime.utcnow()                    # Fecha de emisión
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Compatibilidad entre versiones de PyJWT (bytes o str)
    return token.decode("utf-8") if isinstance(token, bytes) else token


def validar_token(token):
    """
    Valida un token JWT. Devuelve el payload si es válido,
    o None si el token expiró o fue alterado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("⚠️ Token expirado")
        return None
    except jwt.InvalidTokenError:
        print("❌ Token inválido o alterado")
        return None
