from paypal.standard.models import ST_PP_PROCESSED, ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from tickets.models import Ticket
from django.conf import settings
from django.contrib.auth import get_user_model
from events.models import Event
from tickets.models import Ticket
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter




CustomUser = get_user_model()


@receiver(valid_ipn_received)
def paypal_payment_recieved(sender, **kwargs):
    import time
    # Wait 10 secs for paypal to send IPN data
    time.sleep(10)

    paypal_obj = sender
    if paypal_obj.payment_status == ST_PP_COMPLETED:
        user_id = paypal_obj.custom
        user = CustomUser.objects.get(pk=user_id)   
        event_name = paypal_obj.item_name
        event = Event.objects.get(name=event_name)
        if paypal_obj.receiver_email != "business@techconvene.com":
            return False
        if paypal_obj.mc_gross == event.price and paypal_obj.mc_currency == 'USD':
            # Generate a ticket
            ticket = Ticket.objects.create(payment_invoice=paypal_obj.invoice, user=user, 
                                event=event)
            ticket.save()

            fullname = f"{user.first_name}_{user.last_name}"
            filename = f"{fullname}_{ticket.event}.pdf"
            documentTitle = f"{ticket.event}"

            title = f"{ticket.event}"
            headerTile = 'Your Ticket'
            date = f"{ticket.event.date}"
            time = f"{ticket.event.time} Prompt"
            location = f"{ticket.event.venue}"

           
            buffer = io.BytesIO()
            # Create the PDF object, using the buffer as its "file."

            pdf = canvas.Canvas(buffer)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.  
            pdf.setFont('Courier-Bold', 18)
            pdf.drawCentredString(350, 750, title)

            pdf.setTitle(documentTitle)

            pdf.setFont('Courier-Bold', 13)
            pdf.drawString(30, 810, headerTile)

            # Date
            pdf.drawString(30, 700, 'Date')
            pdf.drawString(30, 680, date)

            # Time
            pdf.drawCentredString(305, 700, 'Time')
            pdf.drawCentredString(350, 680, time)

            # Location
            pdf.drawString(30, 640, 'Location')
            pdf.drawString(30, 620, location)


            # Attendee
            pdf.drawString(30, 580, 'Attendee')
            pdf.drawString(30, 560, fullname)


            # Close the PDF object cleanly, and we're done.
            pdf.showPage()
            pdf.save()

            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)
            print(pdf)

            # #Send the email
            email = EmailMessage(
                "Ticket for user",
                "This is your ticket",
                f"{settings.DEFAULT_EMAIL_FROM}",
                ["ibenachoelvis49@gmail.com"],
            )
            # email.attach(filename, pdf, 'application/pdf')
            email.send()
            print(email)
            
    
    else:
        print("Not completed")


