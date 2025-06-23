from django.db.models.signals import post_save
from .models import RoomEvent, Event
from django.dispatch import receiver

@receiver(post_save, sender=Event)
def my_create_room(sender, created, instance, **kwargs):
    if created:
        RoomEvent.objects.create(room_event=instance)
        print(f"The room for the event has been created automatically: {instance.name}")
        instance.save()
