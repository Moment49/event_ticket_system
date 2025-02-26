from django.urls import path
from . import views

urlpatterns = [
    path('tickets/purchased_tickets/', views.purchased_tickets, name="purchased_tickets"),
  
]