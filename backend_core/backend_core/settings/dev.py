from base import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

# During development only, change SMTP email service properties in prod setting
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'