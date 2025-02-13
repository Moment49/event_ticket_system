from django.urls import path
from events import views

urlpatterns = [
    path('event/<int:pk>', views.event_detail_view, name="event_detail"),
    path('event/<int:pk>/payment/', views.payment_process, name="payment"),
]