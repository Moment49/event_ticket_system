from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('auth/login/', views.login_view, name='login'),
    path('auth/register/', views.register, name='register'),
    path('auth/register/account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('auth/register/activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('profile/', views.profile, name="profile"),
    path('profile/edit_profile/<str:username>', views.edit_profile, name="edit_profile"),
    path('dashboard/', views.user_dashboard_view, name='user_dashboard_view'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard_view'),

]