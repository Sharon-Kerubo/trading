from django.urls import re_path
from . import consumers 

websocket_urlpatterns = [
  re_path('ws/(?P<roomname>\w+)/', consumers.ChatConsumer.as_asgi()), # Using asgi
]
