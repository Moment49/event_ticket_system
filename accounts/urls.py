from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('auth/login/', views.login, name='login'),
    path('auth/register/', views.register, name='register')
]