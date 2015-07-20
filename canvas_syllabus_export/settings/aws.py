"""
Django settings for canvas_syllabus_export project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .secure import SECURE_SETTINGS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Base URL for Canvas instance
BASE_URL = SECURE_SETTINGS.get('base_url', "https://canvas.harvard.edu/api")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECURE_SETTINGS.get('secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = SECURE_SETTINGS.get('enable_debug', False)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'syllabuspdf',
    'django_auth_lti',
    'django_app_lti',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_auth_lti.middleware.LTIAuthMiddleware'
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_lti.backends.LTIAuthBackend',
)

# Oauth token for making calls to Canvas API
OAUTH_TOKEN = SECURE_SETTINGS.get("oauthtoken", None)

# Add LTI configuration settings (for django-app-lti)
LTI_SETUP = {
    "TOOL_TITLE": "Syllabus Export",
    "TOOL_DESCRIPTION": "Exports course syllabus as html, with additional option of generating a PDF",
    "LAUNCH_URL": "lti:launch",
    "INITIALIZE_MODELS": False,
    "LAUNCH_REDIRECT_URL": "syllabuspdf:index",
    "EXTENSION_PARAMETERS": {
        "canvas.instructure.com": {
            "privacy_level": "public",
            "course_navigation": {
                "enabled": "true",
                "default": "enabled",
                "text": "Syllabus Export",
                "visibility": "admins"
            }
        }
    }
}

# Add LTI oauth credentials (for django-auth-lti)
LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('lti_oauth_credentials', {})

ROOT_URLCONF = 'canvas_syllabus_export.urls'

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

WSGI_APPLICATION = 'canvas_syllabus_export.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SECURE_SETTINGS.get('db_default_name', 'canvas_syllabus_export'),
        'USER': SECURE_SETTINGS.get('db_default_user', 'canvas_syllabus_export'),
        'PASSWORD': SECURE_SETTINGS.get('db_default_password'),
        'HOST': SECURE_SETTINGS.get('db_default_host', '127.0.0.1'),
        'PORT': SECURE_SETTINGS.get('db_default_port', 5432),
    } 
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'http_static'))
STATIC_URL = '/static/'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

REDIS_HOST = SECURE_SETTINGS.get('redis_host', '127.0.0.1')
REDIS_PORT = SECURE_SETTINGS.get('redis_port', 6379)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': "%s:%s" % (REDIS_HOST, REDIS_PORT),
        'KEY_PREFIX': 'canvas_syllabus_export', # Provide a unique value for shared cache
        'TIMEOUT': SECURE_SETTINGS.get('cache_timeout_in_secs', 60 * 20),
    },
}

# AWS SSL settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'null': {
            "class": 'django.utils.log.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['null', ],
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        'syllabuspdf': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_auth_lti.middleware': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}
