
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import websocketApp.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            websocketApp.routing.websocket_urlpatterns
        )
    ),
})