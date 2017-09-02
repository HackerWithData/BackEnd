"""
Django settings for backend_core project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from clay import config as clay_config
from sqlalchemy.engine.url import URL

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')m##(8z_3^sv@-s-4=0&dkcf(2d1^_afw_5$61e@e%oz*4a1!%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

WEB_APPS = [
    'social_django',
    'contractors',
    'home',
    'users',
    'disk',
    'photos',
    'review',
    'ratings',
]

INSTALLED_APPS = WEB_APPS + PREREQ_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'backend_core.urls'

TEMPLATES_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
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


AUTHENTICATION_BACKENDS = (

    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',

)

WSGI_APPLICATION = 'backend_core.wsgi.application'


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
     os.path.join(BASE_DIR, 'static'),
)
#media file
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

#
LOGIN_REDIRECT_URL = 'home_index'

#AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

SOCIAL_AUTH_GITHUB_KEY = '1d0a444a4e906e9b6373'
SOCIAL_AUTH_GITHUB_SECRET = '324a396f44f7858a9d3fbef208ba6d058f11b19c'

SOCIAL_AUTH_FACEBOOK_KEY = '1571966282825620'
SOCIAL_AUTH_FACEBOOK_SECRET = '6fc15ee3ef0f7a1038d2286ac55847cc'

SOCIAL_AUTH_TWITTER_KEY = 'Jc8Fhb8XDbCygE5ki3GOljNwp'
SOCIAL_AUTH_TWITTER_SECRET = 'aunISCyIzbOr7Lh5iAbYd9qOzjiuLOTYEG6WAtmo7Zs4QYPM32'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '374045419044-2beku5e7dmp46hgrg8ogdanq375th0rh.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '1Q4Jm9Ve_mbbro6quQT3QV7N'
#SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
#SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
#   'https://www.googleapis.com/auth/userinfo.email',
#    'https://www.googleapis.com/auth/userinfo.profile'
#]

SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings/'#home_index
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
