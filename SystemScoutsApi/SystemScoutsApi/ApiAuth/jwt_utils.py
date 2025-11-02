import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = getattr(settings, "SECRET_KEY", "clave_super_secreta")
ALGORITHM = "HS256"
TOKEN_DURATION = timedelta(hours=2)

def generar_token(usuario):
    payload = {
        "user_id": usuario.USU_ID,
        "username": usuario.USU_USERNAME,
        "exp": datetime.utcnow() + TOKEN_DURATION,
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token.decode("utf-8") if isinstance(token, bytes) else token

def validar_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
