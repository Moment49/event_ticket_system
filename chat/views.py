from django.shortcuts import render, redirect
from .models import RoomEvent, ChatMessages
from django.contrib.auth import get_user_model
from django.contrib import messages



# Create your views here.
CustomUser = get_user_model()


def chat_view(request):
    """
    Render the chat landing page
    """
    # Get the event and display the event rooms for GET request
    room_events = RoomEvent.objects.all()

    # Check if a user tries to join a room
    if request.method == 'POST':
        room_event = request.POST.get('room_event')
        # Check if the room exists
        user  = CustomUser.objects.get(email=request.user)
        print(f"test: {user}")
        try:
            room_event = RoomEvent.objects.get(room_event__name__icontains=room_event)
            print(room_event)
        except RoomEvent.DoesNotExist:
            print("Sorry, No such room exists.")
            messages.error(request, "Sorry, No such room exists.")

        # messages.success(request, f"Welcome to the chat room, {username.username}")
        # print(request.user)
        return redirect('chat_room_view', room_event=room_event.room_event.name, username=request.user.username)
        
    return render(request, "chat/chat.html", {"room_events": room_events} )

def chat_room_view(request, room_event, username):
    """
    Render the chat room page for a specific event room
    """
    existing_room_event = RoomEvent.objects.get(room_event__name__icontains=room_event) 
    get_messages = ChatMessages.objects.filter(room=existing_room_event)
    context = {
        "get_messages":get_messages,
        "username":username,
        "room_event":existing_room_event.room_event
    }
    return render(request, 'chat/room_event.html', context)