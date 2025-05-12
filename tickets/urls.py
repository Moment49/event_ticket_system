from django.urls import path
from . import views

urlpatterns = [
    path('tickets/purchased_tickets/', views.purchased_tickets, name="purchased_tickets"),
    path('tickets/purchased_tickets/ticket_pdf/<str:ticket_id>', views.ticket_pdf, name="ticket_pdf"),
    path('tickets/validate_ticket/<str:ticket_id>', views.validate_ticket_qrcode, name="validate-ticket")
  
]