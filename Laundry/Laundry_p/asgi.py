"""
ASGI config for Laundry project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
settings_module = (
    'Laundry_p.deployment_Settings'
    if 'RENDER_EXTERNAL_HOSTNAME' in os.environ
    else 'Laundry_p.settings'
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Laundry_p.settings')

application = get_asgi_application()
