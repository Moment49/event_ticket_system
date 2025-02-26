from paypal.standard.models import ST_PP_PROCESSED, ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from tickets.models import Ticket
from django.conf import settings
import time
from django.contrib.auth import get_user_model
from events.models import Event
from tickets.models import Ticket
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



CustomUser = get_user_model()

@receiver(valid_ipn_received)
def paypal_payment_recieved(sender, **kwargs):
    
    # With 10 secs for paypal to send IPN data
    time.sleep(10)
    paypal_obj = sender
    if paypal_obj.payment_status == ST_PP_COMPLETED:
        user_id = paypal_obj.custom
       
        event_name = paypal_obj.item_name
        event = Event.objects.get(name=event_name)

        if paypal_obj.receiver_email != "business@techconvene.com":
            return False
        if paypal_obj.mc_gross == event.price and paypal_obj.mc_currency == 'USD':
            return True

      
        try:
            event = Event.objects.get(name=event_name)
            user = CustomUser.objects.get(pk=user_id)

        except CustomUser.DoesNotExist and Event.DoesNotExist:
            raise ValidationError("Sorry the user does not exist")
        
        finally:
            ticket = Ticket.objects.create(payment_invoice=paypal_obj.invoice, user=user, 
                                event=event)
            ticket.save()

        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, "Hello world.")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="ticket.pdf")
    
    else:
        print("Not completed")
        

