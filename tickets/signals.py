from paypal.standard.models import ST_PP_PROCESSED, ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from tickets.models import Ticket
from django.conf import settings
import time


@receiver(valid_ipn_received)
def paypal_payment_recieved(sender, **kwargs):
    
    # With 10 secs for paypal to send IPN data
    time.sleep(10)
    paypal_obj = sender
    print(paypal_obj)
    if paypal_obj.payment_status == ST_PP_COMPLETED:
        ...