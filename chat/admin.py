from django.contrib import admin
from .models import RoomEvent, ChatMessages

# Register your models here.

admin.site.register(RoomEvent)
admin.site.register(ChatMessages)
