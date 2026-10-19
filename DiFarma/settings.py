"""
Configuración de Django para el proyecto DiFarma.

Convenciones de este archivo:
- Los secretos y la configuración sensible se leen de variables de entorno
  (ver .env.example); NUNCA se versionan claves reales.
- DEBUG solo se activa en desarrollo mediante DJANGO_DEBUG=True.
- El endurecimiento de seguridad (HSTS, cookies seguras, redirección SSL)
  se activa automáticamente cuando DEBUG=False.
"""
import os
from pathlib import Path

# Ruta base del proyecto: manage.py vive aquí.
BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------------------------------------------------------------
# SEGURIDAD
# ------------------------------------------------------------------------------------------------------------------
# Clave secreta: en producción defínela como variable de entorno.
# El valor por defecto SOLO sirve para desarrollo local.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-cambio-por-variables-de-entorno-solo-desarrollo",
)

# Nunca ejecutes con DEBUG=True en producción.
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")

# Hosts permitidos: en producción lista aquí tu dominio real.
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]


# ------------------------------------------------------------------------------------------------------------------
# APLICACIONES
# ------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Bases",                    # App principal del sistema de farmacia
    "widget_tweaks",            # Renderizado de widgets de formularios en plantillas
    "django.contrib.humanize",  # Filtros de formato numérico (intcomma en tickets)
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "DiFarma.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "DiFarma.wsgi.application"


# ------------------------------------------------------------------------------------------------------------------
# BASE DE DATOS
# ------------------------------------------------------------------------------------------------------------------
# SQLite para desarrollo; para producción cambia a PostgreSQL/MySQL sin tocar el código.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ------------------------------------------------------------------------------------------------------------------
# CONTRASEÑAS
# ------------------------------------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ------------------------------------------------------------------------------------------------------------------
# INTERNACIONALIZACIÓN
# ------------------------------------------------------------------------------------------------------------------
LANGUAGE_CODE = "es-col"        # Español (Colombia)
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True


# ------------------------------------------------------------------------------------------------------------------
# ARCHIVOS ESTÁTICOS
# ------------------------------------------------------------------------------------------------------------------
STATIC_URL = "static/"

# Campo clave por defecto de los modelos.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ------------------------------------------------------------------------------------------------------------------
# ENDURECIMIENTO DE SEGURIDAD (solo producción: DEBUG=False)
# ------------------------------------------------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True          # Fuerza HTTPS
    SESSION_COOKIE_SECURE = True         # Cookie de sesión solo por HTTPS
    CSRF_COOKIE_SECURE = True            # Cookie CSRF solo por HTTPS
    SECURE_HSTS_SECONDS = 3600           # HSTS durante 1 hora (súbelo al desplegar)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
