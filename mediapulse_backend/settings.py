"""
MediaPulse — settings Django
Conforme au Cahier des Charges v2.0 (§2 Architecture technique, §9 Sécurité)
"""

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(key, default=False):
    val = os.environ.get(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


# ------------------------------------------------------------------
# Sécurité de base
# ------------------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-moi-en-production")
DEBUG = env_bool("DEBUG", True)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# ------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Tiers
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    # Apps métier (une par domaine fonctionnel — §10.1 du CdC)
    "core",
    "users",
    "medias",
    "pages",
    "evenements",
    "rapports",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mediapulse_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # templates des rapports PDF (WeasyPrint)
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

WSGI_APPLICATION = "mediapulse_backend.wsgi.application"

# ------------------------------------------------------------------
# Base de données — PostgreSQL partagée (lecture des données de collecte)
# Fallback SQLite si DATABASE_URL absent (confort de dev uniquement)
# ------------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ------------------------------------------------------------------
# Modèle utilisateur personnalisé (email comme identifiant — §4.1 CdC)
# ------------------------------------------------------------------
AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------
# Internationalisation
# ------------------------------------------------------------------
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Fichiers statiques / médias (PDF générés — §2.3 PDF_STORAGE_PATH)
# ------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / os.environ.get("PDF_STORAGE_PATH", "media/rapports/").split("rapports")[0].strip("/") or "media"
PDF_STORAGE_PATH = BASE_DIR / os.environ.get("PDF_STORAGE_PATH", "media/rapports/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------
# Django REST Framework
# ------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": "core.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "core.exceptions.mediapulse_exception_handler",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
}

# ------------------------------------------------------------------
# JWT — durées de vie pilotées par .env (§2.3 / §9.1 du CdC)
# ------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_LIFETIME", 15))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.environ.get("REFRESH_TOKEN_LIFETIME", 7))),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# ------------------------------------------------------------------
# CORS — §9.4 du CdC
# ------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    o.strip() for o in os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",") if o.strip()
]
CORS_ALLOW_METHODS = ["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
CORS_ALLOW_CREDENTIALS = True

# ------------------------------------------------------------------
# Règles métier pilotables par l'environnement (§7.5 du CdC)
# ------------------------------------------------------------------
RAPPORTS_QUOTA_MAX = int(os.environ.get("RAPPORTS_QUOTA_MAX", 3))
RAPPORTS_QUOTA_FENETRE_HEURES = int(os.environ.get("RAPPORTS_QUOTA_FENETRE_HEURES", 4))
RAPPORTS_TIMEOUT_SECONDES = int(os.environ.get("RAPPORTS_TIMEOUT_SECONDES", 120))
