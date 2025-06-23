from django.db import models
from events.models import Event
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class RoomEvent(models.Model):
    """
    Model to represent a room associated with an event.
    """
    room_event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='room_event')

    def __str__(self):
        return f"{self.room_event.name}"


class ChatMessage(models.Model):
    """
    Model to represent a chat message in an event room.
    """
    room = models.ForeignKey(RoomEvent, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"{self.sender}"