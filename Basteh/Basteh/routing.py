from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import authMiddlewarestack

from chat import routing as chat_routing

application = ProtocolTypeRouter({
    'websocket': authMiddlewarestack(
        URLRouter(
            chat_routing.websocket_urlpatterns
        )
    )
})