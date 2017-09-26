from django.conf import settings
from base import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

# TODO: During development only, change SMTP email service properties in prod setting
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Debug toolbar tools
DEV_APPS = [
    'debug_toolbar',
]

INSTALLED_APPS.extend(DEV_APPS)

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ('127.0.0.1',)

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

GOOGLE_API_KEY = 'AIzaSyBcdtc-alvt2fEOMgDk_rmYG03ueIwpurg'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


ALLOWED_HOSTS = [
    'hoome-dev.us-west-2.elasticbeanstalk.com'
]