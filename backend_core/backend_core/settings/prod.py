from base import *

DEBUG = False

# Configuring a SMTP Email Service
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'testsite_app'
# EMAIL_HOST_PASSWORD = 'mys3cr3tp4ssw0rd'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'TestSite Team <noreply@example.com>'

ADMINS = [('maolei', 'tangmaoleismile@gmail.com')]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending e-mail.
EMAIL_HOST = 'smtp.gmail.com'

# Port for sending e-mail.
EMAIL_PORT = 587

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tangmaoleismile@gmail.com'
EMAIL_HOST_PASSWORD = 'tml62285042'


GOOGLE_API_KEY = 'AIzaSyBcdtc-alvt2fEOMgDk_rmYG03ueIwpurg'