from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('auth/login/', views.login_view, name='login'),
    path('auth/register/', views.register, name='register'),
    path('auth/register/account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('auth/register/activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard_view, name='user_dashboard_view'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard_view'),

]