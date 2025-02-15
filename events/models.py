from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.
CustomUser = get_user_model()

class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    featured_photo = models.ImageField(upload_to='uploads/', blank=True, null=True)
    venue = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='event')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ['-created_at']


