from django.shortcuts import render
from events.models import Event
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def event_detail_view(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'events/event_detail.html', {"event":event})


    