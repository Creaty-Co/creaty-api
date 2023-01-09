# imports

import importlib
import logging
import os
from datetime import timedelta
from functools import partial

# noinspection PyPackageRequirements
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from app.base.enums.currency import Currency
from app.base.logs.configs import LogConfig

# env

env = environ.Env(
    ENV_FILE=(str, None),
    DEBUG=bool,
    TEST=bool,
    USE_BROWSABLE_API=bool,
    EMAIL_BACKEND=(str, None),  # default: 'console' if DEBUG else 'smtp'
    CELERY_REDIS_MAX_CONNECTIONS=int,
    CELERY_BROKER_POOL_LIMIT=int,
    CELERY_TASK_EAGER=bool,
    SESSION_ON_LOGIN=bool,
    USE_SILK=bool,
    SILKY_ANALYZE_QUERIES=bool,
    SILKY_PYTHON_PROFILER=bool,
    SILKY_PYTHON_PROFILER_BINARY=bool,
    CLOUDINARY_URL=(str, None),
    SENTRY_DSN=(str, None),
    LOG_CONF={'value': lambda s: s.split(',')},
    LOG_PRETTY=bool,
    LOG_MAX_LENGTH=int,
    LOG_FORMATTERS=dict,
    LOG_LEVEL=dict,
    LOG_REQUESTS=bool,
    ADMINS=({'value': lambda s: s.split(',')}, {}),
    UPDATE_RATES_INTERVAL=(int, 60 * 60 * 8),
)

if (ENV_FILE := env('ENV_FILE')) is not None:
    environ.Env.read_env(ENV_FILE, overwrite=True)

# root

BASE_DIR = environ.Path(__file__) - 2

WSGI_APPLICATION = 'api.wsgi.application'
ASGI_APPLICATION = 'api.asgi.application'
ROOT_URLCONF = 'api.urls'

# site

SITE_NAME = 'Creaty'
SITE_ROOT = BASE_DIR
API_DOMAIN = env('API_DOMAIN')
WEB_DOMAIN = env('WEB_DOMAIN')
DOMAIN = WEB_DOMAIN

# django

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
TEST = env('TEST')
USE_BROWSABLE_API = env('USE_BROWSABLE_API')

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    # third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'django_cleanup',
    'django_pickling',
    'cacheops',
    'silk',
    'cloudinary',
    'cloudinary_storage',
    'drf_spectacular',
    'django_celery_beat',
    'djcelery_email',
    'djmoney',
    'djmoney.contrib.exchange',
    'modeltranslation',
    'django_countries',
    # own apps
    'app.base',
    'app.account',
    'app.admin_',
    'app.mentors',
    'app.tags',
    'app.geo',
    'app.forms',
    'app.mailings',
    'app.pages',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'app.base.renderers.ORJSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'app.base.parsers.ORJSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'app.base.authentications.token.TokenAuthentication',
        'app.base.authentications.session.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'app.base.paginations.page_number.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': env('ANON_THROTTLE_RATE'),
        'user': env('USER_THROTTLE_RATE'),
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

if USE_BROWSABLE_API:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
        'app.base.renderers.BrowsableAPIRenderer'
    ]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # should be as high as possible
    # django middlewares
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # third-party middlewares
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'app.base.middlewares.SilkyMiddleware',
    # own middlewares
    'app.base.middlewares.LogMiddleware',
]

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
            ]
        },
    }
]

# allow

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
INTERNAL_IPS = ['127.0.0.1']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# cache

CACHES = {
    'default': {
        **env.cache('REDIS_URL'),
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    }
}

REDIS_URL = env.cache('REDIS_URL')['LOCATION']

# cacheops

CACHEOPS_REDIS = REDIS_URL

CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60,
    'cache_on_save': True,
    'ops': ['get', 'fetch', 'exists', 'count'],
}
CACHEOPS = {
    'authtoken.*': {'timeout': 60 * 60 * 8},
    'account.*': {'timeout': 60 * 60 * 2},
    'admin_.*': {},
    'geo.*': {'local_get': True},
    'tags.*': {'timeout': 60 * 60 * 4},
    'mentors.*': {},
    'forms.Application': None,
    'forms.*': {'timeout': 60 * 60 * 4},
    'mailings.*': {},
    'pages.*': {'timeout': 60 * 60 * 4},
}

CACHEOPS_DEGRADE_ON_FAILURE = True

# email

EMAIL_HOST: str
EMAIL_PORT: int
EMAIL_USE_SSL: bool
EMAIL_HOST_USER: str | None = None
EMAIL_HOST_PASSWORD: str
EMAIL_BACKEND: str

try:
    vars().update(
        env.email('EMAIL_URL', backend='djcelery_email.backends.CeleryEmailBackend')
    )
except environ.ImproperlyConfigured:
    pass

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# celery_email

CELERY_EMAIL_BACKEND = (
    f"django.core.mail.backends."
    f"{env('EMAIL_BACKEND') or 'console' if DEBUG else 'smtp'}.EmailBackend"
)
CELERY_EMAIL_TASK_CONFIG = {'name': None, 'ignore_result': False}
CELERY_EMAIL_CHUNK_SIZE = 1

# celery[broker]

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=REDIS_URL)

CELERY_TASK_ALWAYS_EAGER = env('CELERY_TASK_EAGER')
CELERY_REDIS_MAX_CONNECTIONS = env('CELERY_REDIS_MAX_CONNECTIONS')
CELERY_BROKER_POOL_LIMIT = env(
    'CELERY_BROKER_POOL_LIMIT', default=CELERY_REDIS_MAX_CONNECTIONS
)
CELERY_REDIS_SOCKET_KEEPALIVE = True

CELERY_TASK_ANNOTATIONS = {'*': {'rate_limit': '10/s'}}
CELERY_TASK_COMPRESSION = 'gzip'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 12 * 60 * 60,
    'max_connections': CELERY_REDIS_MAX_CONNECTIONS,
    'socket_keepalive': True,
}
CELERY_TRACK_STARTED = True
CELERY_TASK_SERIALIZER = 'json'

# celery[result]

CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default=REDIS_URL)

CELERY_RESULT_COMPRESSION = CELERY_TASK_COMPRESSION
CELERY_RESULT_ACCEPT_CONTENT = ['json']
CELERY_IGNORE_RESULT = False

# celery beat

CELERY_BEAT_SCHEDULE = {
    'update_rates': {
        'task': 'geo.tasks.update_rates',
        'schedule': timedelta(seconds=env('UPDATE_RATES_INTERVAL')),
    }
}

# media

USE_CLOUDINARY = False
if (CLOUDINARY_URL := env('CLOUDINARY_URL')) != 'cloudinary://0:stub@_':
    USE_CLOUDINARY = True
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {'PREFIX': env('CLOUDINARY_PREFIX')}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + 'media'
DATA_UPLOAD_MAX_MEMORY_SIZE = None

# static

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + 'static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# silk

USE_SILK = env('USE_SILK', default=DEBUG)
SILKY_INTERCEPT_FUNC = lambda _: USE_SILK  # noqa: E731
SILKY_MIDDLEWARE_CLASS = 'app.base.middlewares.SilkyMiddleware'
SILKY_MAX_RECORDED_REQUESTS = 100_000
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_META = True
SILKY_HIDE_COOKIES = False
SILKY_ANALYZE_QUERIES = env('SILKY_ANALYZE_QUERIES')
SILKY_EXPLAIN_FLAGS = {
    'format': 'JSON',
    'costs': True,
    'verbose': True,
    'buffers': True,
}
SILKY_SENSITIVE_KEYS = {'𘚠'}
SILKY_PYTHON_PROFILER = env('SILKY_PYTHON_PROFILER')
SILKY_PYTHON_PROFILER_BINARY = env('SILKY_PYTHON_PROFILER_BINARY')
SILKY_PYTHON_PROFILER_RESULT_PATH = BASE_DIR + 'profiles/'
if USE_SILK and not os.path.exists(SILKY_PYTHON_PROFILER_RESULT_PATH):
    os.makedirs(SILKY_PYTHON_PROFILER_RESULT_PATH)

# sentry

if (SENTRY_DSN := env('SENTRY_DSN')) is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            LoggingIntegration(
                level=logging.DEBUG,
                event_level=logging.ERROR,
            ),
            DjangoIntegration(),
            RedisIntegration(),
        ],
        environment=env('SENTRY_ENVIRONMENT'),
        traces_sample_rate=1.0,
        attach_stacktrace=True,
        send_default_pii=True,
        request_bodies='always',
        _experiments={
            'profiles_sample_rate': 1.0,
        },
    )

# swagger

SPECTACULAR_SETTINGS = {
    'TITLE': f'{SITE_NAME} API',
    'DISABLE_ERRORS_AND_WARNINGS': True,
}

# db

DATABASES = {'default': env.db()}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# redirects

REDIRECT_ON_UNSUBSCRIBE = env('REDIRECT_ON_UNSUBSCRIBE')

# auth

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'account.User'
SESSION_ON_LOGIN = env('SESSION_ON_LOGIN', bool, DEBUG)

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# logs

LOG_ADMINS = {
    v[0]: list(map(lambda s: s.lower(), v[1:])) for v in env('ADMINS').values()
}
ADMINS = [(name, email__levels[0]) for name, email__levels in env('ADMINS').items()]
EMAIL_SUBJECT_PREFIX = f'{SITE_NAME} logger > '

LOG_FORMATTERS = env('LOG_FORMATTERS')
LOG_PRETTY = env('LOG_PRETTY')
LOG_MAX_LENGTH = env('LOG_MAX_LENGTH')
LOG_REQUESTS = env('LOG_REQUESTS')

_loggers = {
    k: {
        'handlers': list(
            map(
                partial(
                    getattr,
                    importlib.import_module('.handlers', 'app.base.logs.configs'),
                ),
                v,
            )
        )
    }
    for k, v in env('LOG_CONF').items()
}
for k, v in env('LOG_LEVEL').items():
    _loggers.setdefault(k, {})['level'] = v

LOGGING = LogConfig(_loggers).to_dict()

# language

USE_I18N = True

LANGUAGES = [('ru', 'Русский'), ('en', 'Английский')]

MODELTRANSLATION_TRANSLATION_FILES = ['api.translation']

# money

CURRENCIES = tuple(map(str, Currency))
CURRENCY_CHOICES = Currency.choices
DEFAULT_CURRENCY = str(Currency.USD)

EXCHANGE_BACKEND = 'djmoney.contrib.exchange.backends.FixerBackend'
FIXER_ACCESS_KEY = env('FIXER_ACCESS_KEY')

# timezone

TIME_ZONE = 'UTC'
USE_L10N = True
USE_TZ = True
