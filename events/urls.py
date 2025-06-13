from django.urls import path
from events import views

urlpatterns = [
    path('event/<str:pk>', views.event_detail_view, name="event_detail"),
    path('events/booked_events', views.booked_event, name="booked_event"),
    path('payment/success/', views.payment_success, name="payment_sucesss"),
]