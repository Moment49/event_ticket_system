from django.shortcuts import render
from events.models import Event
from tickets.models import Ticket
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
# Create your views here.

CustomUser = get_user_model()

@login_required
def event_detail_view(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'events/event_detail.html', {"event":event})

@login_required
def saved_event_qrcodes(request):
    return render(request, 'events/saved_qrcodes.html')

@login_required
def booked_event(request):
    user = CustomUser.objects.get(email=request.user)
    user_tickets_events = Ticket.objects.select_related('event').filter(user=user)
    
    # Get the total number of events based on the tickets purchased
    booked_event_count = user_tickets_events.count()
   
    return render(request, 'events/booked_events.html', 
                  {"user_tickets_events":user_tickets_events, 
                   "booked_event_count":booked_event_count})


    