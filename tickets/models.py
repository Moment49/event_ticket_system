from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event
import uuid


CustomUser = get_user_model()

# Create your models here.
class Payment(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    )
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS, default='Pending')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='payment')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='payment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount}"
    
    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_invoice = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ticket')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='tickets')
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event.name}"

    class Meta:
        ordering = ["-created_at"]
