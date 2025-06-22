from django.urls import path
from .views import chat_view


urlpatterns = [
    path("meet/", chat_view, name="chat_view")
]