from django.urls import path
from .consumers import ChatConsumer

wspattern = [
    path('ws/messages/<str:room_name>/', ChatConsumer.as_asgi())
]