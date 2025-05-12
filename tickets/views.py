from django.shortcuts import render, redirect, HttpResponse
import qrcode.constants
from tickets.models import Ticket, Payment
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode
from django.contrib.sites.shortcuts import get_current_site
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from accounts.views import is_admin


CustomUser = get_user_model()

def ticket_pdf(request, ticket_id):
    # Create a file-like buffer to receive PDF data.
    ticket = Ticket.objects.get(ticket_id=ticket_id)

    user = CustomUser.objects.get(email=request.user)
    fullname = f"{user.first_name} {user.last_name}"
    filename = f"{fullname}_{ticket.event}.pdf"
    documentTitle = f"{ticket.event}"

    title = f"{ticket.event}"
    headerTile = 'Your Ticket'
    date = ticket.event.date.strftime("%A, %d %B %Y")
    print(date)
   
    time = f"{ticket.event.time.strftime('%I:%M:%S %p')} Prompt"
    location = f"{ticket.event.venue}"


    # Get abs path of the image
    image = ticket.event.featured_photo.path
    print(image)

    # embed QRcode
    # get the absolute domain and url for the ticket to validate
    protocol = "https" if request.is_secure() else 'http'
    print(protocol)
    ticket_valid_url_to_qrcode = protocol + ':' + '//' + get_current_site(request).domain + ticket.get_absolute_url()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(ticket_valid_url_to_qrcode)
    qr.make(fit=True)
    buffer = io.BytesIO()
    qr_code_image = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_code_image.save(buffer, format="PNG")
    buffer.seek(0)
  
   # Create the PDF object, using the buffer as its "file."
    pdf = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.  
    pdf.setFont('Courier-Bold', 18)
    pdf.drawCentredString(340, 750, title)

    pdf.setTitle(documentTitle)

    # fonts = pdf.getAvailableFonts()
    # print(fonts)

    # Convert the Image path for the event pic and qrcode ticket to be readable by Reportlab
    featured_photo = ImageReader(image)
    qrcode_reader = ImageReader(qr_code_image)
   

    pdf.drawImage(featured_photo, 30, 720, width=80, height=75)
    pdf.setFont('Courier-Bold', 13)
    pdf.drawString(30, 810, headerTile)

    # Qrcode Image
    pdf.drawImage(qrcode_reader, 270, 470, width=220, height=200)

    # Date
    pdf.setFont('Courier', 13)
    pdf.drawString(30, 700, 'Date')
    pdf.drawString(30, 680, date)

    # Time
    pdf.drawCentredString(305, 700, 'Time')
    pdf.drawCentredString(360, 680, time)

    # Location
    pdf.drawString(30, 640, 'Location')
    pdf.drawString(30, 620, location)


    # Attendee details
    pdf.drawString(30, 560, 'Attendee Details')
    pdf.drawString(30, 520, 'Attendee')
    pdf.drawString(30, 500, fullname)

   

    # Close the PDF object cleanly, and we're done.
    pdf.showPage()
    pdf.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)



@login_required
def purchased_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)

    # count the tickets
    tickets_count = tickets.count()
    return render(request, 'tickets/purchased_tickets.html', {"tickets":tickets, "tickets_count":tickets_count})



@user_passes_test(is_admin)
@login_required
def validate_ticket_qrcode(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket_date = ticket.event.date

    ticket_year = ticket_date.year
    ticket_month = ticket_date.month
    ticket_day = ticket_date.day

    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day
   
    if (current_year, current_month, current_day) >= (ticket_year, ticket_month, ticket_day):
        print("Ticket is validated")
        # Mark the ticket as been used
        if ticket.is_used == True:
            messages.error(request, "Sorry ticket has already been used")
        else:
            # mark the ticke for the first time as used
            ticket.is_used = True
            ticket.save()
            messages.success(request, 'Ticket is validated...')
    else:
        print("Sorry wait till the event date..")
        messages.error(request, 'Sorry wait till the event date..')
    

    return render(request, 'tickets/validate_tickets_info.html', {"ticket":ticket})

