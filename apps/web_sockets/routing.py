from .consumers import SocketConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/data/', SocketConsumer.as_asgi()),
]
