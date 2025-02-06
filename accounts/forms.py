from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Firstname"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Lastname"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"your-email@example.com"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password", 'required':True}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1']
    

    def clean_password1(self):
        password_data = self.cleaned_data['password1']
        password_data2 = self.cleaned_data['password2']

        if len(password_data) < 8 or len(password_data2):
            raise ValidationError('Password must be 8 characters and above')
        
        return password_data
    
        

    

