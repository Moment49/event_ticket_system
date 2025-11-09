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
from django.views.decorators.cache import cache_page
from django.core.cache import cache


# Create your views here.

CustomUser = get_user_model()

@login_required
def event_detail_view(request, pk):
    event = Event.objects.get(event_id=pk)
    ticket = Ticket.objects.select_related("event").filter(user__email=request.user)

    price = event.price

    # The domain_host address
    host = request.get_host()
    user = CustomUser.objects.get(email=request.user)
    user_id = user.pk

    # The paypal data to be filled dynamically to process the information
    paypal_checkout = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount': price,
        'item_name':event.name,
        'invoice':uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url':f"https://{host}{reverse('paypal-ipn')}",
        'return_url':f"http://{host}{reverse('payment_sucesss')}",
        'cancel_url':f"http://{host}{reverse('event_detail', kwargs={'pk':event.event_id})}",
        'custom':user_id
    }

    
    if not ticket.exists():
        form = PayPalPaymentsForm(initial=paypal_checkout)
        context = {"event":event, "form":form}
    else:
        if not ticket.filter(event_id=pk).exists():
            form = PayPalPaymentsForm(initial=paypal_checkout)
            context = {"event":event, "form":form}
        else:
            context = {"event":event}

    return render(request, 'events/event_detail.html', context)

@login_required
def payment_success(request):
    return render(request, 'events/payment_success.html')



@login_required
def booked_event(request):
    user = CustomUser.objects.get(email=request.user)
    
    # print(user_tickets_events)
    cached_key = f"user_tickets_events_{user.id}"
    
    if cache.get(cached_key):
        user_tickets_events = cache.get(cached_key)
    
    else:
        user_tickets_events = Ticket.objects.select_related('event').filter(user=user)

        # Get the total number of events based on the tickets purchased
        cache.set(cached_key, user_tickets_events, timeout=60 * 15)

    booked_event_count = user_tickets_events.count()

    return render(request, 'events/booked_events.html',
                   {"booked_event":booked_event_count, "user_tickets_events":user_tickets_events})


    