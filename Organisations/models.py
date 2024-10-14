from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

# Organisation model to manage different organisations
class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Organisation name
    org_admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organisation')  # Associate with a primary user
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the organisation was created

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create or get the Group with the same name as the organisation
        group, created = Group.objects.get_or_create(name=self.name)

        # Assign the organisation admin to the group
        if self.org_admin and group not in self.org_admin.groups.all():
            self.org_admin.groups.add(group)
            print(f"{self.org_admin.username} added to group '{self.name}'.")

    def __str__(self):
        return self.name
    
# UserProfile model to store additional user information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

# Get or create UserProfile for a user
def get_or_create_user_profile(user):
    """Get the UserProfile for a given user, creating it if it doesn't exist."""
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile

# Signal to create a new group when an organisation is created
@receiver(post_save, sender=Organisation)
def create_organisation_group(sender, instance, created, **kwargs):
    if created:
        # Create a Group with the same name as the organisation
        Group.objects.get_or_create(name=instance.name)
        print(f"Group '{instance.name}' created.")