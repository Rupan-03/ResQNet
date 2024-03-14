import os
from django.core.asgi import get_asgi_application

from logging import basicConfig,DEBUG

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rescueNet.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter

from rescuenetApp.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app, 
    "websocket":URLRouter(websocket_urlpatterns),
})

#basicConfig(level=DEBUG)
