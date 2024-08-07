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

# patches

__import__('api._patch_django_cleanup')

# env

env = environ.Env(
    ENV_FILE=(str, '.env'),
    DEBUG=bool,
    TEST=bool,
    USE_BROWSABLE_API=bool,
    USE_DEBUG_TOOLBAR=bool,
    EMAIL_BACKEND=(str, None),  # default: 'console' if DEBUG else 'smtp'
    CELERY_REDIS_MAX_CONNECTIONS=int,
    CELERY_BROKER_POOL_LIMIT=int,
    CELERY_TASK_EAGER=bool,
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

if (ENV_FILE := env('ENV_FILE')) is not None and os.path.isfile(ENV_FILE):
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
PLATFORM_API_URL = env('PLATFORM_API_URL')
ROOT_DOMAIN = '.'.join(WEB_DOMAIN.split('.')[-2:])
DOMAIN = WEB_DOMAIN

# django

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
TEST = env('TEST')
USE_BROWSABLE_API = env('USE_BROWSABLE_API')
USE_DEBUG_TOOLBAR = env('USE_DEBUG_TOOLBAR')
APPEND_SLASH = False

INSTALLED_APPS = [
    'admin_interface',  # must be before django.contrib.admin
    'colorfield',  # must be before django.contrib.admin
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
    'social_django',
    'cloudinary',
    'cloudinary_storage',
    'drf_spectacular',
    'django_celery_beat',
    'djcelery_email',
    'djmoney',
    'djmoney.contrib.exchange',
    'django_countries',
    'rest_framework_simplejwt',
    'debug_toolbar',
    # own apps
    'app.base',
    'app.users',
    'app.admin_',
    'app.mentors',
    'app.tags',
    'app.geo',
    'app.forms',
    'app.mailings',
    'app.pages',
    'app.bookings',
    'app.platform',
    'app.calendar',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['app.base.renderers.ORJSONRenderer'],
    'DEFAULT_PARSER_CLASSES': [
        'app.base.parsers.ORJSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'app.base.authentications.session.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'app.base.paginations.page_number.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.AnonRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {'anon': env('ANON_THROTTLE_RATE')},
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

if USE_BROWSABLE_API:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
        'app.base.renderers.BrowsableAPIRenderer'
    ]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # should be as high as possible
    'django.middleware.security.SecurityMiddleware',  # immediately after CorsMiddleware
    # django middlewares
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # third-party middlewares
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

DEBUG_TOOLBAR_CONFIG = {
    'IS_RUNNING_TESTS': False,
    'SHOW_TOOLBAR_CALLBACK': lambda _: USE_DEBUG_TOOLBAR,
}

# cache

CACHES = {
    'default': {
        **env.cache('REDIS_CACHE_URL', backend='django_redis.cache.RedisCache'),
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    },
    'storage': {
        **env.cache('REDIS_STORAGE_URL', backend='django_redis.cache.RedisCache'),
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    },
}

# cacheops

CACHEOPS_REDIS = env('REDIS_CACHEOPS_URL')

CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60,
    'cache_on_save': True,
    'ops': ['get', 'fetch', 'exists', 'count'],
}
CACHEOPS = {
    'users.*': {},
    'geo.*': {'timeout': 60 * 60 * 24},
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

try:
    vars().update(env.email('EMAIL_URL'))
except environ.ImproperlyConfigured:
    pass

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
DEFAULT_FROM_EMAIL = f'"Creaty.club" <{EMAIL_HOST_USER}>'

# celery_email

CELERY_EMAIL_BACKEND = (
    f"django.core.mail.backends."
    f"{env('EMAIL_BACKEND') or 'console' if DEBUG else 'smtp'}.EmailBackend"
)
CELERY_EMAIL_TASK_CONFIG = {'name': None, 'ignore_result': False}
CELERY_EMAIL_CHUNK_SIZE = 1

# celery[broker]

CELERY_BROKER_URL = env('REDIS_CELERY_URL')

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

CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_RESULT_COMPRESSION = CELERY_TASK_COMPRESSION
CELERY_RESULT_ACCEPT_CONTENT = ['json']
CELERY_IGNORE_RESULT = False

# celery beat

CELERY_BEAT_SCHEDULE = {
    'update_rates': {
        'task': 'app.geo.tasks.update_rates',
        'schedule': timedelta(seconds=env('UPDATE_RATES_INTERVAL')),
    },
    'check_health': {
        'task': 'app.base.tasks.check_health',
        'schedule': timedelta(minutes=1),
    },
}

# media

DEFAULT_MEDIA_STORAGE = 'app.base.storages.file_system.FileSystemStorage'

USE_CLOUDINARY = False
if (CLOUDINARY_URL := env('CLOUDINARY_URL')) != 'cloudinary://0:stub@_':
    USE_CLOUDINARY = True
    DEFAULT_MEDIA_STORAGE = 'app.base.storages.cloudinary.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {'PREFIX': env('CLOUDINARY_PREFIX')}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + 'media'
DATA_UPLOAD_MAX_MEMORY_SIZE = None

# static

STORAGES = {
    'default': {'BACKEND': DEFAULT_MEDIA_STORAGE},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + 'static'

# sentry


def _traces_sampler(sampling_context):
    if (
        sampling_context.get('celery_job', {}).get('task')
        == 'app.base.tasks.check_health'
    ):
        return 0
    if sampling_context.get('asgi_scope', {}).get('path') == '/base/status/':
        return 0
    if sampling_context.get('wsgi_environ', {}).get('PATH_INFO') == '/base/status/':
        return 0
    return 1


if (SENTRY_DSN := env('SENTRY_DSN')) is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            LoggingIntegration(level=logging.DEBUG, event_level=logging.ERROR),
            DjangoIntegration(),
            RedisIntegration(),
        ],
        environment=env('SENTRY_ENVIRONMENT'),
        traces_sampler=_traces_sampler,
        attach_stacktrace=True,
        send_default_pii=True,
        max_request_body_size='always',
        _experiments={'profiles_sample_rate': 1},
    )

# swagger

SPECTACULAR_SETTINGS = {
    'TITLE': f'{SITE_NAME} API',
    'DISABLE_ERRORS_AND_WARNINGS': True,
}

# db

DATABASES = {'default': env.db(), 'platform': env.db('PLATFORM_DATABASE_URL')}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# redirects

REDIRECT_ON_UNSUBSCRIBE = env('REDIRECT_ON_UNSUBSCRIBE')

# auth

AUTH_PASSWORD_VALIDATORS = []

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=12),
}

VERIFICATION_REGISTER_FAILURE_PATH = ''
VERIFICATION_REGISTER_SUCCESSFUL_PATH = 'email-verified'

VERIFICATION_PASSWORD_RESET_FAILURE_PATH = ''
VERIFICATION_PASSWORD_RESET_SUCCESSFUL_PATH = 'user/reset-password'

# social_auth

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('GOOGLE_APP_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('GOOGLE_APP_SECRET')
SOCIAL_AUTH_GOOGLE_SCOPE = ['email']
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/calendar.events',
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]
SOCIAL_AUTH_GOOGLE_PROFILE_EXTRA_PARAMS = {'fields': 'id, name, email'}
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'include_granted_scopes': 'true',
    'prompt': 'consent',
}

SOCIAL_AUTH_STRATEGY = 'app.users.strategy.SocialStrategy'
SOCIAL_AUTH_USER_FIELDS = ['email', 'first_name', 'last_name']
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['first_name', 'last_name']

SOCIAL_AUTH_LOGIN_REDIRECT_URL = f"https://{WEB_DOMAIN}"

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'app.users.pipelines.user_details',
)

# logs

LOG_FORMATTERS = env('LOG_FORMATTERS')
LOG_PRETTY = env('LOG_PRETTY')
LOG_MAX_LENGTH = env('LOG_MAX_LENGTH')
LOG_REQUESTS = env('LOG_REQUESTS')

_loggers: dict = {
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
