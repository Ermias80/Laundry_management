"""
WSGI config for Laundry project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
settings_module = (
    'Laundry.deployment_Settings'
    if 'RENDER_EXTERNAL_HOSTNAME' in os.environ
    else 'Laundry.settings'
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'Laundry.settings'))


application = get_wsgi_application()
