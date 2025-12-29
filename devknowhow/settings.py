import os
import environ
import mimetypes
from pathlib import Path
from corsheaders.defaults import default_headers


BASE_DIR = Path(__file__).resolve().parent.parent

mimetypes.add_type("text/css", ".css", True)

env = environ.Env()
environ.Env.read_env()


SECRET_KEY = env("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", "True") == "True"

if DEBUG:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
    CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")
    CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS_PROD")
    CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS_PROD")
    CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS_PROD")

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    import sentry_sdk
    sentry_sdk.init(
        dsn=env("SENTRY_URL"),
        send_default_pii=True,
        traces_sample_rate=1.0,
        profile_session_sample_rate=1.0,
        profile_lifecycle="trace",
        ignore_errors=[
            "django.core.exceptions.DisallowedHost",
        ],
    )

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
REFERRER_POLICY = "no-referrer"

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'baggage',
    'sentry-trace',
]

ROOT_URLCONF = 'devknowhow.urls'

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
    'option',
    'creator',
    'message',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

LANGUAGE_CODE = 'en'

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