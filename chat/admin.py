from django.contrib import admin
from .models import RoomEvent, ChatMessage

# Register your models here.

admin.site.register(RoomEvent)
admin.site.register(ChatMessage)
