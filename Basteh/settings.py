import os
from datetime import timedelta
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
environ.Env.read_env()

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'account',
    'advertise',
    'chat',
    'payment',
    'fcm_django',
]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'billlig.com',
    '193.141.64.9',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '200/day',  #TODO
        'user': '1000/day'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6
}

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

ROOT_URLCONF = 'Basteh.urls'

# Is this needed ? TODO
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

WSGI_APPLICATION = 'Basteh.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

DATABASES = {
    'default': env.db(),
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/dstatic/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'dstatic/static/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'dstatic/'), 
)

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'dstatic/media/')

# Check this TODO
CORS_ORIGIN_ALLOW_ALL = True

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# CACHES = {
#     'default': env.cache('REDIS_URL'),
#     'redis': env.cache('REDIS_URL')
# }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SITE_ID = 1 

AUTH_USER_MODEL='account.User'


FCM_DJANGO_SETTINGS = {
         # default: _('FCM Django')
        "APP_VERBOSE_NAME": "[string for AppConfig's verbose_name]",
         # Your firebase API KEY
        "FCM_SERVER_KEY": env("FCM_SECRET_KEY"),
         # true if you want to have only one active device per registered user at a time
         # default: False
        "ONE_DEVICE_PER_USER": False,
         # devices to which notifications cannot be sent,
         # are deleted upon receiving error response from FCM
         # default: False
        "DELETE_INACTIVE_DEVICES": False,
}

kavenegar_api = env('kavenegar_api')
vandar_api = env('vandar_api')
vandar_mobile = env('vandar_mobile')
vandar_password = env('vandar_password')

CSRF_COOKIE_SECURE = True

# To avoid transmitting the session cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

# SECURE_CONTENT_TYPE_NOSNIFF = True

# SECURE_SSL_REDIRECT = True

# SECURE_HSTS_SECONDS = 86400  # 1 day

# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURE_HSTS_PRELOAD = True

# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#     }
# }