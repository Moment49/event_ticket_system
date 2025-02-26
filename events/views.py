from django.shortcuts import render, redirect
from events.models import Event
from tickets.models import Ticket
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
# Create your views here.


CustomUser = get_user_model()

@login_required
def event_detail_view(request, pk):
    event = Event.objects.get(event_id=pk)
  
    price = event.price
    # Check if the user has purchased the ticket for the event
    ticket_user = Ticket.objects.filter(user__email=request.user)
    for ticket in ticket_user:
        if event == ticket.event:
            print("User have registered for the event already")
            messages.error(request, "Sorry you have registered for the event already")
    # The domain_host address
    host = request.get_host()

    # The paypal data to be filled dynamically to process the information
    paypal_checkout = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount': price,
        'item_name':event.name,
        'invoice':uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url':f"https://{host}{reverse('paypal-ipn')}",
        'return_url':f"http://{host}{reverse('payment_sucesss')}",
        'cancel_url':f"http://{host}{reverse('event_detail', kwargs={'pk':event.event_id})}"

    }
    form = PayPalPaymentsForm(initial=paypal_checkout)

    return render(request, 'events/event_detail.html',  {
                "event":event,
                'form':form})


@login_required
def payment_success(request):
    return render(request, 'events/payment_success.html')

@login_required
def saved_event_qrcodes(request):
    return render(request, 'events/saved_qrcodes.html')

@login_required
def booked_event(request):
    # user = CustomUser.objects.get(email=request.user)
    # user_tickets_events = Ticket.objects.select_related('event').filter(user=user)
    
    # # Get the total number of events based on the tickets purchased
    # booked_event_count = user_tickets_events.count()
   
    return render(request, 'events/booked_events.html')


    