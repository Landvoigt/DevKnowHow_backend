from pathlib import Path
import os
import environ
import mimetypes

BASE_DIR = Path(__file__).resolve().parent.parent

mimetypes.add_type("text/css", ".css", True)

env = environ.Env()
environ.Env.read_env()


SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '212.227.161.51',
    '212.227.161.51:8000',
    'server-timvoigt.ch',
    'www.server-timvoigt.ch',
    'timvoigt.ch',
    'devknowhow.timvoigt.ch',
]

INSTALLED_APPS = [
    # other
    'corsheaders',
    'modeltranslation',

    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # rest-framework
    'rest_framework',

    # apps
    'category',
    'command',
    'routine',
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

CSRF_TRUSTED_ORIGINS = [
  'http://127.0.0.1:5500',
  'http://localhost:5500',
  'http://127.0.0.1:8000',
  'http://localhost:8000',
  'http://localhost:4200',
  'https://server-timvoigt.ch',
]

CORS_ALLOWED_ORIGINS = [
  'http://localhost:4200',
  'http://localhost:8000',
  'https://timvoigt.ch',
  'https://devknowhow.timvoigt.ch',
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'devknowhow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'devknowhow/templates'],
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

WSGI_APPLICATION = 'devknowhow.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

STATIC_URL = '/static/devknowhow/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('de', gettext('German')),
)