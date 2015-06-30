"""
Django settings for syllabusexport project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .secure import SECURE_SETTINGS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    'django.contrib.sessions',
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
LTI_OAUTH_CREDENTIALS = {
    "mykey":"mysecret",
    "myotherkey": "myothersecret",
}

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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
STATIC_ROOT = '/home/ubuntu/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = ('/home/ubuntu/canvas-syllabus-export/canvas_syllabus_export/syllabuspdf/static', )


