"""
ASGI config for ticketsphere_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import wspattern

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsphere_project.settings')

http_response_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http":http_response_app,
    "websocket": URLRouter(wspattern)
})