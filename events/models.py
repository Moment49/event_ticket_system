from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
CustomUser = get_user_model()

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    featured_photo = models.ImageField(upload_to='uploads/', blank=True, null=True)
    venue = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='event')
