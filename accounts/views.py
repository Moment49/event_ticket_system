from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import get_user_model
from django.contrib import messages



CustomUser = get_user_model()


# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')

def login(request):
    return render(request, 'accounts/login.html')

def activateEmail(request, user, to_email):
    messages.success(request, f'Dear, {user} Please go to your email <b>{to_email}</b> inbox and click\
                     on the recieved activation link to complete the registeration process. <b>Note:</b>Check your spam folder')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  
        if form.is_valid():
            print(form)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            print(user)
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'Successfully registered')
            return redirect('login')
        else:
            messages.error(request, "EErrors")


    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form':form})
