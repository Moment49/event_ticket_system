from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event


CustomUser = get_user_model()

# Create your models here.
class Payment(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    )
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=STATUS, default='Pending')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='payment')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='payment')

    def __str__(self):
        return f"{self.status}"


class Ticket(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='ticket')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ticket')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='tickets')

    def __str__(self):
        return f"{self.event.name}"
