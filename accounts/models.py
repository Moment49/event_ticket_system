from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name=None, last_name=None):
        if not email:
            raise ValueError("Email is required")
        if not first_name:
            raise ValueError("First_name is required")
        if not last_name:
            raise ValueError("Last_name is required")
        if not password:
            raise ValueError('Password is required')
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, first_name=None, last_name=None):
        user = self.create_user(email, password, first_name, last_name)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)

        return user

class CustomUser(AbstractUser):
    ROLES = (
        ('USER', 'User'),
        ('EVENT-ORGANIZER', 'Event-organizer'),
        ('ADMIN', 'Admin'))
    role = models.CharField(max_length=20, choices=ROLES, default='USER')
    email = models.CharField(max_length=150, unique=True, null=False, blank=False)
    username = models.CharField(max_length=100, unique=False, null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    profile_picture = models.ImageField(upload_to='media/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user