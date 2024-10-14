# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update the UserProfile whenever the User is saved."""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Update the existing UserProfile if the User is updated
        instance.profile.save()  # Ensure to use the related name defined in UserProfile
