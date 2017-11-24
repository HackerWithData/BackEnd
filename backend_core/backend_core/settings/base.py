# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.messages import constants as messages

"""
Django settings for backend_core project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')m##(8z_3^sv@-s-4=0&dkcf(2d1^_afw_5$61e@e%oz*4a1!%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '52.38.54.17',
    '52.88.186.98',
    'ebdbtest.cpqxzirsz2nd.us-west-2.rds.amazonaws.com',
    'SSLLoadBalancer-2138526934.us-west-2.elb.amazonaws.com',
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
    '.hoome.io',
    'hoome.io',
    'www.hoome.io',
]

# Application definition

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'storages',
    'tinymce',
    'rest_framework',
    # 'django_scss',
]

AUTH_APPS = [
    # The following apps are required:
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # include the providers you want to enable:
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]

WEB_APPS = [
    # 'social_django',
    'contractors',
    'home',
    'users',
    'photos',
    'review',
    'ratings',
    'search',
    'professionals',
    'architects',
    'designers',
    'rule',
    'career',
    'dashboard',
    "hscore",
    'projects',
    'transactions',
    'overviews'
]

INSTALLED_APPS = WEB_APPS + AUTH_APPS + PREREQ_APPS

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
                "django.template.context_processors.i18n",
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'search.context_processors.global_settings',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
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

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/',
    }
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# customized user model
AUTH_USER_MODEL = 'users.User'

SITE_ID = 8888

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQURIED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_FORMS = {'signup': 'users.forms.UserSignUpForm'}

# auth and all allauth settings
LOGIN_REDIRECT_URL = 'home_index'
LOGOUT_REDIRECT_URL = 'home_index'

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4',
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SOCIAL_AUTH_FACEBOOK_APP_ID = '526289131044788'
SOCIAL_AUTH_FACEBOOK_SECRET = '94390bde88a2e5fac03c9eb7828ef3bf'

SOCIAL_AUTH_GITHUB_KEY = '1d0a444a4e906e9b6373'
SOCIAL_AUTH_GITHUB_SECRET = '324a396f44f7858a9d3fbef208ba6d058f11b19c'

SOCIAL_AUTH_TWITTER_KEY = 'Jc8Fhb8XDbCygE5ki3GOljNwp'
SOCIAL_AUTH_TWITTER_SECRET = 'aunISCyIzbOr7Lh5iAbYd9qOzjiuLOTYEG6WAtmo7Zs4QYPM32'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '167647890871-46behgrf3g0hkda1o5oe1r77bbtjdchf.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '_NErMjXqKFPkf0WKWt90fnVV'

SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings/'
# home_index
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('zh-hans', u'简体中文'),
    ('zh-hant', u'繁体中文'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'extra_locales', 'allauth'),
)

GOOGLE_RECAPTCHA_SECRET_KEY = '6LdWazUUAAAAANWO1-wzqu7GII4QGp084y-2_qjq'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'modern',
    'plugins': 'paste searchreplace autosave',
    'width': 'auto',
    'height': 288,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'elementpath': False
}
# 'autoresize_min_height': 300,
# 'autoresize_max_height': 350,
TINYMCE_COMPRESSOR = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
TINYMCE_JS_URL = STATIC_ROOT + ('tinymce/plugin')

FORTE_CONFIG = {
    'api_login_id': 'qCt61J81jU',
    'secure_trans_key': 'hv3TJ3BG5q4',
    'method': 'sale',
    'version_number': '1.0',
    'allowed_methods': 'echeck',
    'hash_method': 'md5',
    'billing_company_name': 'hide',
}