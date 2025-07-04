from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileForm, UserForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.token import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from accounts.models import UserProfile
from events.models import Event
from django.views.decorators.cache import cache_page
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin


CustomUser = get_user_model()

# Create your views here.


def home(request):
    event_ = Event.objects.all().first()
    print(event_)
    return render(request, 'accounts/home.html', {"event_":event_})

def activateEmail(request, user, to_email):
    subject = 'Activate your account'
    message = render_to_string(
        'accounts/activate_email_account.html',
        context={
            'user': user.first_name,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )

    email = EmailMessage(subject, message, to=[to_email])
    return email


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, 'Thank you for your email confirmation. Now you can login to your account')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid')

    return redirect('home')
      


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  
        if form.is_valid():
            user = form.save(commit=False)
            # Set the user as inactivate until after verification
            user.is_active = True
            # Save the user
            user.save()
           
            email = activateEmail(request, user, form.cleaned_data.get('email'))
            
            if email.send():
                # send the email and return the user to
                return redirect("account_activation_sent")
            else:
                messages.error(request, f'Problem sending email to {user.email}, check if you typed it correctly.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form':form})

def is_regular_user(user):
    if user.role == 'USER':
        return user

def is_admin(user):
    if user.role == 'ADMIN':
        return user

@login_required    
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/dashboard/admin_dashboard_view.html', {"users":users})

# @cache_page(5)
@login_required
@user_passes_test(is_regular_user)
def user_dashboard_view(request):
    events = Event.objects.all()
    return render(request, 'accounts/dashboard/user_dashboard_view.html', {"events":events})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful...')
            if user.role == 'ADMIN':
                print(user.role)
                return redirect('admin_dashboard_view')
            if user.role == 'USER':
                return redirect('user_dashboard_view')
        else:
            messages.error(request, 'Sorry, Invalid crendentials..')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!!!')
    return redirect('login')


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')

class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {"user_profile":user_profile})

def edit_profile(request, username):
    user = CustomUser.objects.get(username=username)
    print(username)
    user_profile = UserProfile.objects.get(user=user)
   
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        user_form = UserForm(request.POST)
        print(user_form)
        if form.is_valid() and user_form.is_valid():
            date_of_birth = form.cleaned_data.get('date_of_birth')
            profile_picture = form.cleaned_data.get('profile_picture')
            first_name = user_form.cleaned_data.get('first_name')
            last_name = user_form.cleaned_data.get('last_name')
            username = user_form.cleaned_data.get('username')

            user_profile.date_of_birth = date_of_birth
            user_profile.profile_picture = profile_picture
            user.first_name = first_name
            user.last_name = last_name
            user.username = username

            user.save()
            user_profile.save()
            messages.success(request, "profile updated successfully..")
            return redirect('profile')
    else:
        form = ProfileForm({
            "date_of_birth":user_profile.date_of_birth,
            "profile_picture":user_profile.profile_picture})
        user_form = UserForm({
            "first_name":user.first_name,
            "last_name":user.last_name,
            "username":user.username,
        })
    return render(request, 'accounts/edit_profile.html', {"form":form, "user_form":user_form})


