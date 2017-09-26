"""
WSGI config for backend_core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
sys.path.insert(0, '/opt/python/current/app/backend_core')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_core.settings.prod")

application = get_wsgi_application()
