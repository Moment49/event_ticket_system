from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from accounts.models import UserProfile

CustomUser = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Firstname"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Lastname"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"your-email@example.com"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password", 'required':True}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
    

    def clean_password(self):
        password_data = self.cleaned_data['password']
        SpecialSym =['$', '@', '#', '%']
        if len(password_data) < 8:
            raise ValidationError('Password must be 8 characters and above')
        if not any(char.isdigit() for char in password_data):
            raise ValidationError('Password must contain a digit')
        if not any(char.islower() for char in password_data):
            raise ValidationError("Password must conatin a lowercase letter")
        if not any(char.isupper() for char in password_data):
            raise ValidationError("Password must contain an uppercase letter")
        if not any(char in SpecialSym for char in password_data):
            raise ValidationError("Password must conatin a special characters")
        
        return password_data
    
    def save(self, commit=False):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'profile_picture']

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']   

    

