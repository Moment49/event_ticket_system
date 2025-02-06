from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

CustomUser = get_user_model()

@receiver(post_save, sender=CustomUser)
def create_profile(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print(f"Profile for user {instance.email} created")
        instance.save()