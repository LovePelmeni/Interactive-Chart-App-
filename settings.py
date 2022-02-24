"""
Django settings for ChartProject project.
Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
# import environ
# env = environ.env()
# print(env.db())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lb6ulotywlue!#xx-q(sz873467bdcu29wj8n1!jmoocav&$fw1_#a9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',

    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
    'rest_framework',
    'crispy_forms',
]

AUTHENTICATION_BACKENDS = (

    'chat.backends.BaseAdminAuthBackend',
    'chat.backends.BaseAuthBackend',
    'django.contrib.auth.backends.ModelBackend',

)
ALLOW_FILED_CACHE = False # To Allow Filed Based Cache, replace it with True...

REST_FRAMEWORK = {

    'DEFAULT_RENDERER_CLASSES': [

        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVStreamingRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',

    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    ),

    'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAdminUser',
    ),
    'PAGINATE_BY': 10,

    }

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'compression_middleware.middleware.CompressionMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGGING = {

    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {

        'chart_formatter': {

            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        }
    },
    'handlers': {

        'chart_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'chart_log.log',
            'formatter': 'chart_formatter'
        },
    },
    'loggers': {
        'main': {
            'handlers': ['chart_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

ROOT_URLCONF = 'ChartProject.urls'

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

ASGI_APPLICATION = 'ChartProject.asgi.application'
WSGI_APPLICATION = 'ChartProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('CHART_DB_NAME'),
        'USER': os.getenv('CHART_DB_USER'),
        'PASSWORD': os.getenv('CHART_DB_PASSWORD'),

        'HOST': 'localhost',
        'PORT': '5432',
    }
}

if ALLOW_FILED_CACHE:

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(BASE_DIR, 'chart_cache'),
        }
    }

else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'main/static/')
STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'main/static/images/')
MEDIA_URL = 'main/static/images/'


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'