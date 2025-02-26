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
# from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse
from django.conf import settings


CustomUser = get_user_model()


@login_required
def purchased_tickets(request):
    return render(request, 'tickets/purchased_tickets.html')