import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

http_application = get_asgi_application()
application = ProtocolTypeRouter({
  'http': http_application,
  'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})
