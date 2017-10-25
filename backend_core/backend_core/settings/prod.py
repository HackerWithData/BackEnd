from django.core.exceptions import ImproperlyConfigured
from requests.exceptions import ConnectionError

from base import *
import requests

DEBUG = False

# Configuring a SMTP Email Service
ADMINS = [('Moore', 'tangmaoleismile@gmail.com'),
          ('Jeremy', 'jeremyzheng@hoome.io')]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending e-mail.
EMAIL_HOST = 'smtp.gmail.com'

# Port for sending e-mail.
EMAIL_PORT = 587

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'service@hoome.io'
EMAIL_HOST_PASSWORD = 'CZT!2017'

GOOGLE_API_KEY = 'AIzaSyBcdtc-alvt2fEOMgDk_rmYG03ueIwpurg'

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
            'OPTIONS': {
                'init_command': 'SET default_storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci'
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'hoome_local',
            'USER': 'root',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': 'SET default_storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci'
            }
        }
    }

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'www', 'media')

"""
AWS S3 settings
This will tell boto that when it uploads files to S3, it should set properties on them so
that when S3 serves them, it'll include some HTTP headers in the response. Those HTTP headers,
in turn, will tell browsers that they can cache these files for a very long time.
"""
AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}

AWS_STORAGE_BUCKET_NAME = 'hoomeincstatic'
AWS_S3_REGION_NAME = 'us-west-2'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = 'AKIAJPC6XIUMQZIR2CQQ'
AWS_SECRET_ACCESS_KEY = 'mqHtIuhnkiXRq1upZ59vugQmktPWsLtn/1vHJ0Kv'

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'backend_core.settings.custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'backend_core.settings.custom_storages.MediaStorage'

# ALLOWED_HOSTS
url = "http://169.254.169.254/latest/meta-data/public-ipv4"
try:
    r = requests.get(url)
    instance_ip = r.text
    ALLOWED_HOSTS += [instance_ip]
except ConnectionError:
    error_msg = "You can only run production settings on an AWS EC2 instance"
    raise ImproperlyConfigured(error_msg)
# END ALLOWED_HOSTS
