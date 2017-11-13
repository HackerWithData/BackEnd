from django.conf import settings
from base import *


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = (
     os.path.join(BASE_DIR, 'static'),
)
#media file
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# test data
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

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
# DEV_APPS = [
#     'debug_toolbar',
# ]

# INSTALLED_APPS.extend(DEV_APPS)
#
# MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ('127.0.0.1',)

# def show_toolbar(request):
#     return True

# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": show_toolbar,
# }

GOOGLE_API_KEY = 'AIzaSyBcdtc-alvt2fEOMgDk_rmYG03ueIwpurg'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Forte test account configure
FORTE_CONFIG = {
    'api_login_id': 'HPBuBdGvU',
    'secure_trans_key': 'mPJHiA51HQS93X',
    'method': 'sale',
    'version_number': '1.0',
    'allowed_methods': 'visa, mast, disc, amex, echeck',
    'hash_method': 'md5',
}
