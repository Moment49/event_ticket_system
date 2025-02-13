from django.shortcuts import render
from events.models import Event
from tickets.models import Ticket, Payment
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def event_detail_view(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'events/event_detail.html', {"event":event})

def payment_process(request, pk):
    event = Event.objects.get(pk=pk)
    
    Payment.objects.create()
    