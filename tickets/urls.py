from django.urls import path
from . import views

urlpatterns = [
    path('event/<int:pk>/payment/', views.payment_process, name="payment"),
    path('payment/success/', views.payment_success, name="payment_sucesss"),
    path('tickets/purchased_tickets/', views.purchased_tickets, name="purchased_tickets"),
  
]