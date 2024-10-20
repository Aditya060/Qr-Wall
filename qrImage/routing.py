# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import RevealConsumer

websocket_urlpatterns = [
    path('ws/reveal/', RevealConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})
