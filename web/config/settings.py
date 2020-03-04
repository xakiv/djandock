import os

from decouple import config, Csv

from .logger import LOGGING  # NOQA


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', cast=Csv())


# Application definition

CORE_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
]

THIRD_PARTY_DJANGO_APPS = config('THIRD_PARTY_DJANGO_APPS', default='', cast=Csv())

OUR_APPS = config('OUR_APPS', default='', cast=Csv())

INSTALLED_APPS = CORE_APPS + THIRD_PARTY_DJANGO_APPS + OUR_APPS

CORE_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
]

OUR_MIDDLEWARE = config('OUR_MIDDLEWARE', default='', cast=Csv())

MIDDLEWARE = CORE_MIDDLEWARE + OUR_MIDDLEWARE


ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': config("ENGINE"),
        'NAME': config("NAME"),
        'USER': config("USER"),
        'PASSWORD': config("PASSWORD"),
        'HOST': config("HOST"),
        'PORT': config("PORT"),
        'OPTIONS': {
            'options': '-c search_path=djandock,public'
        },
    },
    'switch': {
        'ENGINE': config("ENGINE"),
        'NAME': config("NAME"),
        'USER': config("USER"),
        'PASSWORD': config("PASSWORD"),
        'HOST': config("HOST"),
        'PORT': config("PORT"),
        'OPTIONS': {
            'options': '-c search_path=switch,public'
        },
    },
}

DATABASE_ROUTERS = config('DATABASE_ROUTERS', default='', cast=Csv())

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Site

SITE_ID = 1

# Email confs

EMAIL_BACKEND = config(
    'EMAIL_BACKEND', default="django.core.mail.backends.console.EmailBackend")

EMAIL_HOST = config('EMAIL_HOST')

EMAIL_HOST_USER = config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

EMAIL_PORT = config('EMAIL_PORT', cast=int)

EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Geocontrib conf

AUTH_USER_MODEL = 'geocontrib.User'

LOGIN_URL = 'geocontrib:login'

LOGIN_REDIRECT_URL = 'geocontrib:index'

LOGOUT_REDIRECT_URL = 'geocontrib:index'

APPLICATION_NAME = "Géocontrib"

APPLICATION_ABSTRACT = "Application collaborative"

IMAGE_FORMAT = "application/pdf,image/png,image/jpeg"

# Notification frequency (allowed values: 'never', 'instantly', 'daily', 'weekly')
DEFAULT_SENDING_FREQUENCY = config('GEOCONTRIB_DEFAULT_SENDING_FREQUENCY', default='never')

LOGO_PATH = config('GEOCONTRIB_LOGO_PATH', default=os.path.join(MEDIA_URL, 'logo.png'))

# Allowed formats for file attachments
IMAGE_FORMAT = config('GEOCONTRIB_IMAGE_FORMAT', default='application/pdf,image/png,image/jpeg')

# Max size of file attachments
FILE_MAX_SIZE = config('GEOCONTRIB_FILE_MAX_SIZE', default=10000000)

DEFAULT_BASE_MAP = {
    'SERVICE': 'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',
    'OPTIONS': {
        'attribution': '&copy; contributeurs d\'<a href="https://osm.org/copyright">OpenStreetMap</a>',
        'maxZoom': 20
    }
}

DEFAULT_MAP_VIEW = {
    'center': [50.00976, 2.8657699],
    'zoom': 7
}

# IdeO BFC conf

HEADER_UID = config('HEADER_UID', default=None)

OIDC_SETTED = config('OIDC_SETTED', default=False, cast=bool)
