from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
import itrader.routing


application = ProtocolTypeRouter({
    'websocket' : AuthMiddlewareStack(
            URLRouter(
                itrader.routing.websocket_urlpatterns
        )
    ),
})