from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # other websocket URLs here
    # as_asgi() is for using Django Channels(Consumer) class as an ASGI application.
    path(r"ws/chatgpt-demo/", consumers.ChatConsumer.as_asgi(), name="chatgpt_demo"),
]