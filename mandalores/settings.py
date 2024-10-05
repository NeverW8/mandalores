"""
Django settings for mandalores project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from os import getenv

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.envrc')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY', 'django-insecure-(2l-z)2&*j$)+nzvhqe^9$5&!ib)^=hmcny8+l+7knbqwy0(dv')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('ENV', 'local') == 'local'

ALLOWED_HOSTS = [
    getenv('ALLOWED_HOST', 'localhost')
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mandalores',
    'mandalores.soundboard_clip_generator',
    'mandalores.emoji_resizer',
    'mandalores.media_material',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mandalores.urls'

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

AUTHENTICATION_BACKENDS = [
    'mandalores.auth.backends.DiscordOAuth2AuthorizationBackend',
]

WSGI_APPLICATION = 'mandalores.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mandalores',
        'USER': 'mandalores',
        'PASSWORD': getenv('DB_PASSWORD', 'mysecretpassword'),
        'HOST': getenv('DB_HOST', 'localhost'),
        'PORT': getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'sv-se'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / "assets",
]

MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Discord OAuth2 settings
DISCORD_CLIENT_ID = getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = getenv("DISCORD_REDIRECT_URI")
DISCORD_WEBHOOK_URL = getenv("DISCORD_WEBHOOK_URL")

DISCORD_DEFAULT_ALLOWED_USERS = ["fiskenhero", "soew", "exosist", "johndoh"]

DISCORD_API_ENDPOINT = 'https://discord.com/api/v10'
DISCORD_OAUTH_AUTHORIZE_ENDPIONT = 'https://discord.com/api/oauth2/authorize'

LOGIN_URL = '/login/'
