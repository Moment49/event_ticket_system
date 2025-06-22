from django.shortcuts import render

# Create your views here.

def chat_view(request):
    """
    Render the chat landing page
    """
    return render(request, "chat/chat.html")