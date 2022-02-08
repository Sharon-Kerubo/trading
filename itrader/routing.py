from django.urls import re_path
from . import consumers 

websocket_urlpatterns = [
  re_path('ws/(?P<room_name>\w+)/', consumers.ChatConsumer.as_asgi()), # Using asgi
]
