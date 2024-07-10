"""
ASGI config for youtube_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# Asynchronous Sever Gateway Interface

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_chat.settings')

application = get_asgi_application()

# setting for asgi_application (routingapp)
from chat_generator.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    websocket_urlpatterns,  # add this alongside other routes.
                )
            )
        ),
    }
)