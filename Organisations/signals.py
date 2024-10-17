# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from register.models import UserProfile

@receiver(post_save, sender=UserProfile)  # Change sender to UserProfile
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal that ensures a UserProfile is created for new users and updated if the user already exists.
    """
    # If the UserProfile is newly created
    if created:
        # Here you might want to perform any specific actions needed on UserProfile creation
        print(f"UserProfile created for user: {instance.user.username}")
    else:
        # Update logic can be added here if needed
        print(f"UserProfile updated for user: {instance.user.username}")