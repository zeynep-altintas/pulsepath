"""
ASGI config for pulsepath project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # ✅ Required for WebSockets
from channels.layers import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pulsepath.settings")
django.setup()

from pulsepath.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(  # ✅ Add this to handle authentication in WebSockets
            URLRouter(websocket_urlpatterns)
        ),
    }
)

channel_layer = get_channel_layer()