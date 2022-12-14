import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
IS_HEROKU = "DYNO" in os.environ

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.getenv("DEBUG", False)

# Heroku router provides hostname validation
if IS_HEROKU:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'storages',
    'drf_spectacular',

    'pizza'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MAX_CONN_AGE = 600

if "DATABASE_URL" in os.environ:
    # Configure Django for DATABASE_URL environment variable.
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=MAX_CONN_AGE, ssl_require=True)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "static/"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'UserSnack Django REST Backend',
    'DESCRIPTION': 'Backend to serve pizzas and take pizza orders for Usersnack',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

CORS_ALLOWED_ORIGINS = [
    "https://usersnack-frontend.vercel.app",
    "http://localhost:3000",
]

if IS_HEROKU:
    # Image storage for heroku
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
