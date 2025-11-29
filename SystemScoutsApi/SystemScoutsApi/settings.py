from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Configurar PyMySQL como reemplazo de MySQLdb
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# Read DEBUG from env, convert to boolean. Default to True for local dev.
DEBUG = str(os.getenv("DEBUG_API", "True")).lower() in ("1", "true", "yes")

# Allow localhost addresses by default for development. Can be overridden
# by setting an environment variable named ALLOWED_HOSTS (comma-separated).
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")


# Application definition

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
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
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

# Allow frontend dev server origins (vite default port 5173/5174) and enable
# credentials so cookies or other credentialed requests work during development.
CORS_ALLOW_CREDENTIALS = True


ROOT_URLCONF = 'SystemScoutsApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DATABASE"),
        'USER': os.getenv("USER"),
        'PASSWORD': os.getenv("PASSWORD_DB"),
        'HOST': os.getenv("HOST"),
        'PORT': os.getenv("PORT", "3306"),
        'OPTIONS': {
            # Ensure connection uses utf8mb4 to correctly handle accents and ñ
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', NAMES 'utf8mb4'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 0,
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}

# Deshabilitar verificación de versión para MariaDB 10.4
import django.db.backends.mysql.base
django.db.backends.mysql.base.DatabaseWrapper.check_database_version_supported = lambda self: None

AUTHENTICATION_BACKENDS = [
    'ApiCoreScouts.authentication.UsuarioBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SIMPLE_JWT = {
    "USER_ID_FIELD": "USU_ID",
    "USER_ID_CLAIM": "user_id",
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

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
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
