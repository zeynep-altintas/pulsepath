from django.urls import re_path
from .consumers import CrowdConsumer

websocket_urlpatterns = [
    re_path(r"ws/crowd-density/$", CrowdConsumer.as_asgi()),
]
