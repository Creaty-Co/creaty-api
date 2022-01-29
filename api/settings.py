"""
Environment requirements:
    Django:
        *SECRET_KEY:
            :type: str
        DEBUG:
            :type: bool
            :default: False
        TEST:
            :type: bool
            :default: False
    
    Email:
        *EMAIL_URL:
            :type: str
            :pattern: smtp(+ssl)?://.+
        EMAIL_BACKEND:
            :type: str
            :choices:
                console
                smtp
            :default: console
    
    Database:
        *DATABASE_URL:
            :type: str
            :pattern: psql://.+
    
    Redis:
        *REDIS_URL:
            :type: str
            :pattern: redis://.+
        CELERY_REDIS_MAX_CONNECTIONS:
            :type: int
            :default: 10
    
    Environ:
        ENV_FILE:
            :type: str
    
    Logs:
        LOG_CONF:
            :type: dict
            :pattern: logger=handler,...;...
            :default: {'api': ['api_console'], 'django.server': ['web_console']}
        LOG_LEVEL: dict
        LOG_FORMATTERS:
            :type: dict
            :pattern: logger=format;...
            :default: {
                'api': '%(levelname)-8s| %(name)s %(asctime)s '
                       '<%(module)s->%(funcName)s(%(lineno)d)>: %(message)s',
                'web': 'WEB     | %(asctime)s: %(message)s'
            }
        LOG_PRETTY:
            :type: bool
            :default: True
        LOG_MAX_LENGTH:
            :type: int
            :default: 130
        ADMINS:
            :type: dict
            :pattern: name=email,level,...;...
            :default: {}
"""

###
# imports

import importlib
from functools import partial

# noinspection PyPackageRequirements
import environ

from base.logs.configs import LogConfig

# imports
###

###
# env

_env_value = {'value': lambda s: s.split(',')}
_localhost = 'http://localhost:8000/'

env = environ.Env(
    ENV_FILE=(str, None),
    DEBUG=(bool, False),
    TEST=(bool, False),
    EMAIL_BACKEND=(str, None),
    LOG_CONF=(_env_value, {'api': ['api_console'], 'django.server': ['web_console']}),
    LOG_PRETTY=(bool, True),
    LOG_MAX_LENGTH=(int, 130),
    LOG_FORMATTERS=(dict, {
        'api': '%(levelname)-8s| %(name)s %(asctime)s <%(module)s->%(funcName)s(%('
               'lineno)d)>: %(message)s',
        'web': 'WEB     | %(asctime)s: %(message)s'
    }),
    LOG_LEVEL=(dict, {}),
    CELERY_REDIS_MAX_CONNECTIONS=(int, 10),
    VERIFICATION_CODE_TIMEOUT=(int, 86400),
    ADMINS=(_env_value, {}),
    TRAVELPAYOUTS_MARKER=int,
    VERIFICATION_ACTIVATE_SUCCESS_URL=(str, _localhost),
    VERIFICATION_ACTIVATE_FAILURE_URL=(str, _localhost),
    SOCIAL_AUTH_LOGIN_REDIRECT_URL=(str, _localhost),
    SOCIAL_REDIRECT_URL=(str, _localhost)
)

if env('ENV_FILE'):
    environ.Env.read_env(env_file=env('ENV_FILE'))

# env
###

###
# root

SETTINGS_PATH = environ.Path(__file__)
BASE_DIR = SETTINGS_PATH - 2

WSGI_APPLICATION = (SETTINGS_PATH - 1)().split('\\')[-1].split('/')[-1] + \
                   '.wsgi.application'
ROOT_URLCONF = (SETTINGS_PATH - 1)().split('\\')[-1].split('/')[-1] + '.urls'

# root
###

###
# site

SITE_ROOT = BASE_DIR
SITE_NAME = 'Creaty'

# site
###

###
# django

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
TEST = env('TEST')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'drf_spectacular',
    'cacheops',
    'django_cleanup.apps.CleanupConfig',
    'djcelery_email',
    'modeltranslation',
    'django_pickling',
    *(['debug_toolbar'] if DEBUG else []),
    
    'django.contrib.admin',
    
    'base'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'app.accounts.authentications.token.TokenAuthentication',
        'app.accounts.authentications.session.SessionAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'base.paginations.base.BasePagination',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {'anon': '1000/s', 'user': '10000/s'},
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    *(['debug_toolbar.middleware.DebugToolbarMiddleware'] if DEBUG else []),
    
    'base.middlewares.RequestLogMiddleware'
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
                'django.contrib.messages.context_processors.messages'
            ]
        }
    }
]

# django
###

###
# allow

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
INTERNAL_IPS = ['127.0.0.1']

# allow
###

###
# cache

CACHES = {
    'default': {
        **env.cache('REDIS_URL'),
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'}
    }
}

REDIS_URL = env.cache('REDIS_URL')['LOCATION']

# cache
###

###
# cacheops

CACHEOPS_REDIS = REDIS_URL

CACHEOPS_DEFAULTS = {
    'timeout': 60 * 5, 'cache_on_save': True, 'ops': ['get', 'fetch', 'exists']
}
CACHEOPS = {
    # 'account.*': {}  TODO
}

CACHEOPS_DEGRADE_ON_FAILURE = True

# cacheops
###

###
# email

EMAIL_HOST: str
EMAIL_PORT: int
EMAIL_USE_SSL: bool
EMAIL_HOST_USER: str
EMAIL_HOST_PASSWORD: str
EMAIL_BACKEND: str

vars().update(
    env.email('EMAIL_URL', backend='djcelery_email.backends.CeleryEmailBackend')
)

# email
###

###
# celery_email

CELERY_EMAIL_BACKEND = f"django.core.mail.backends" \
                       f".{env('EMAIL_BACKEND') or 'console' if DEBUG else 'smtp'}" \
                       f".EmailBackend"
CELERY_EMAIL_TASK_CONFIG = {
    'name': None,
    'ignore_result': False
}
CELERY_EMAIL_CHUNK_SIZE = 1

# celery_email
###

###
# celery

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=REDIS_URL)
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default=REDIS_URL)

CELERY_REDIS_MAX_CONNECTIONS = env('CELERY_REDIS_MAX_CONNECTIONS')
CELERY_REDIS_SOCKET_KEEPALIVE = True

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 20, 'max_connections': CELERY_REDIS_MAX_CONNECTIONS,
    'socket_keepalive': True
}
CELERY_BROKER_POOL_LIMIT = 0

CELERY_RESULT_SERIALIZER = 'json'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False
CELERY_TRACK_STARTED = True
CELERYD_LOG_LEVEL = 'INFO'

# celery
###

###
# media

MEDIA_URL = '/media/'
DATA_UPLOAD_MAX_MEMORY_SIZE = None

# media
###

###
# static

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# static
###

###
# swagger

SPECTACULAR_SETTINGS = {
    'TITLE': f'{SITE_NAME} API',
    'VERSION': '1.0'
}

# swagger
###

###
# db

DATABASES = {'default': env.db()}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# db
###

###
# auth

AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6}
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

# AUTH_USER_MODEL = 'account.User'  TODO
SESSION_ON_LOGIN = env('SESSION_ON_LOGIN', bool, DEBUG)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

# auth
###

###
# logs

LOG_ADMINS = {v[0]: list(map(lambda s: s.lower(), v[1:])) for v in env('ADMINS').values()}
ADMINS = [(name, email__levels[0]) for name, email__levels in env('ADMINS').items()]
EMAIL_SUBJECT_PREFIX = f'{SITE_NAME} logger > '

LOG_FORMATTERS = env('LOG_FORMATTERS')
LOG_PRETTY = env('LOG_PRETTY')
LOG_MAX_LENGTH = env('LOG_MAX_LENGTH')

_loggers = {
    k: {
        'handlers': list(
            map(
                partial(
                    getattr,
                    importlib.import_module('.handlers', 'app.main.logs.configs')
                ), v
            )
        )
    } for k, v in env('LOG_CONF').items()
}
for k, v in env('LOG_LEVEL').items():
    _loggers.setdefault(k, {})['level'] = v

LOGGING = LogConfig(_loggers).to_dict()

# logs
###

###
# language

LANGUAGES = (
    ('ru', 'Русский'),
    ('en', 'Английский')
)

# MODELTRANSLATION_TRANSLATION_FILES = (
#     'api.translation',
# )

USE_I18N = True

# language
###

###
# timezone

TIME_ZONE = 'UTC'
USE_L10N = True
USE_TZ = True

# timezone
###
