import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if RENDER_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_HOSTNAME]
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_HOSTNAME}"]
else:
    ALLOWED_HOSTS = ['localhost']
    CSRF_TRUSTED_ORIGINS = []

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Use this if you're on Django 4.2+
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Use this if you're on Django 3.x
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}