from django.shortcuts import render, redirect
from tickets.models import Ticket, Payment
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
import uuid
from django.urls import reverse
from django.conf import settings
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import qrcode
from django.core.paginator import Paginator


CustomUser = get_user_model()

def ticket_pdf(request, ticket_id):
    # Create a file-like buffer to receive PDF data.
    ticket = Ticket.objects.get(ticket_id=ticket_id)

    user = CustomUser.objects.get(email=request.user)
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
    email = EmailMessage(
                "Ticket for user",
                "This is your ticket",
                f"{settings.DEFAULT_EMAIL_FROM}",
                ["ibenachoelvis49@gmail.com"],
            )
            # email.attach(filename, pdf, 'application/pdf')
    email.send()
    print(email)
    return FileResponse(buffer, as_attachment=True, filename=filename)



@login_required
def purchased_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)

    # count the tickets
    tickets_count = tickets.count()
    return render(request, 'tickets/purchased_tickets.html', {"tickets":tickets, "tickets_count":tickets_count})