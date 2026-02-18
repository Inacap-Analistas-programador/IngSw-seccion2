from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path
import os
from pathlib import Path
from decouple import Config, RepositoryEnv, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIST = BASE_DIR / 'frontend' / 'dist'
FRONTEND_DIST_EXISTS = (FRONTEND_DIST / 'index.html').exists()

# cargar los distintos archivos .env
env_names = ['.env', 'env']
env_path = None

for name in env_names:
    candidate = BASE_DIR / name
    if candidate.exists():
        env_path = candidate
        break
    candidate = BASE_DIR.parent / name
    if candidate.exists():
        env_path = candidate
        break

class ChainedRepository:
    """
    Repository that looks in os.environ first, then the provided repository (file).
    This ensures that hosting variables override .env files, and both are available.
    """
    def __init__(self, file_repo=None):
        self.file_repo = file_repo
        self.system_env = os.environ

    def __contains__(self, key):
        return key in self.system_env or (self.file_repo and key in self.file_repo)

    def __getitem__(self, key):
        if key in self.system_env:
            return self.system_env[key]
        if self.file_repo and key in self.file_repo:
            return self.file_repo[key]
        raise KeyError(key)

file_repository = None
if env_path and env_path.exists():
    try:
        file_repository = RepositoryEnv(env_path, encoding='utf-8')
    except UnicodeDecodeError:
        # fallback al encoding
        file_repository = RepositoryEnv(env_path, encoding='latin-1')
else:
    print(f"⚠️  Warning: .env file not found. Relying on environment variables.")

# Create config that defaults to os.environ, falling back to .env file
config = Config(ChainedRepository(file_repository))

# CONFIGURACION BASICA
# Default to development mode if no configuration is found
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
DEPLOY_SECRET = config('DEPLOY_SECRET', default='temp-secret-change-me')

# SECRET_KEY configuration with secure defaults
# In production (DEBUG=False), SECRET_KEY MUST be provided via environment variable
# In development (DEBUG=True), a fallback is allowed for convenience
if DEBUG:
    SECRET_KEY = config('DJANGO_SECRET_KEY', default='dev-secret-key-change-in-production')
else:
    SECRET_KEY = config('DJANGO_SECRET_KEY')

if not DEBUG:
    # Configuraciones de seguridad para producción
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='api.guiasyscoutsbiobio.cl,www.api.guiasyscoutsbiobio.cl,guiasyscoutsbiobio.cl,www.guiasyscoutsbiobio.cl,localhost,127.0.0.1,testserver', cast=Csv())


# APLICACIONES INSTALADAS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ApiCoreScouts',
    
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'django_filters',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'scout_project.security_middleware.SecurityHeadersMiddleware',
    # 'scout_project.security_middleware.XSSProtectionMiddleware',
    # 'scout_project.security_middleware.SecurityLoggingMiddleware',
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "accept",
    "origin",
    "user-agent",
    "dnt",
    "cache-control",
    "x-requested-with",
]

# PERMITIR EL USO DE CREDENCIALES Y COOKIES 
CORS_ALLOW_CREDENTIALS = True

# CACHE DE PREFLIGHT (24 horas)
CORS_PREFLIGHT_MAX_AGE = 86400

# Enable automatic slash append to fix 404s when client omits trailing slash
APPEND_SLASH = True

ROOT_URLCONF = 'SystemScoutsApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [FRONTEND_DIST],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SystemScoutsApi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Use SQLite as fallback if MySQL settings are not provided
DB_NAME = config("DATABASE", default=config("DB_NAME", default=None))
DB_HOST = config("HOST", default=config("DB_HOST", default=None))

if DB_NAME and DB_HOST:
    # MySQL configuration when credentials are provided
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': config("DB_USER", default="MISSING_DB_USER"),
            'PASSWORD': config("DB_PASSWORD", default="MISSING_DB_PASSWORD"),
            'HOST': DB_HOST,
            'PORT': config("PORT", default="3306"),
            'OPTIONS': {
                # Ensure connection uses utf8mb4 to correctly handle accents and ñ
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES', NAMES 'utf8mb4'",
                'charset': 'utf8mb4',
            },
            'CONN_MAX_AGE': 0,
            'DISABLE_SERVER_SIDE_CURSORS': True,
        }
    }
else:
    # SQLite fallback for development/testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Deshabilitar verificación de versión para MariaDB 10.4 (solo cuando se usa MySQL)
if DB_NAME and DB_HOST:
    import django.db.backends.mysql.base
    django.db.backends.mysql.base.DatabaseWrapper.check_database_version_supported = lambda self: None

AUTHENTICATION_BACKENDS = [
    'ApiCoreScouts.authentication.UsuarioBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SIMPLE_JWT = {
    "USER_ID_FIELD": "usu_id",
    "USER_ID_CLAIM": "user_id",
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

AUTH_USER_MODEL = 'ApiCoreScouts.Usuario'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'ApiCoreScouts': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Keep CORS allowed origins consistent. Include both localhost and 127.0.0.1
# for ports used by the frontend dev server (5173, 5174).
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "https://api.guiasyscoutsbiobio.cl",
    "https://sistema.guiasyscoutsbiobio.cl",
    "https://guiasyscoutsbiobio.cl",
    "https://www.guiasyscoutsbiobio.cl",
]

CSRF_TRUSTED_ORIGINS = [
    "https://api.guiasyscoutsbiobio.cl",
    "https://sistema.guiasyscoutsbiobio.cl",
    "https://guiasyscoutsbiobio.cl",
    "https://www.guiasyscoutsbiobio.cl",
]

# Email configuration
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@guiasyscoutsbiobio.cl')
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Site URL for QR codes and external links
SITE_URL = config('SITE_URL', default='https://api.guiasyscoutsbiobio.cl')


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
