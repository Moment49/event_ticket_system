from django.urls import path
from .views import chat_view, chat_room_view


urlpatterns = [
    path("meet/", chat_view, name="chat_view"),
    path("meet/<str:room_event>/<str:username>/", chat_room_view, name="chat_room_view")
]