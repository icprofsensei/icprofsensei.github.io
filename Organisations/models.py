from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group


# Organisation model to manage different organisations
class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Organisation name
    password = models.CharField(max_length=128, default='temporary_default_password') 
    org_admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organisation')  # Associate with a primary user
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the organisation was created

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.pk is None:  # Only hash the password if the object is being created
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        # Create or get the Group with the same name as the organisation
        group, created = Group.objects.get_or_create(name=self.name)

        # Assign the organisation admin to the group
        if self.org_admin and group not in self.org_admin.groups.all():
            self.org_admin.groups.add(group)
            print(f"{self.org_admin.username} added to group '{self.name}'.")

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


# Signal to create a new group when an organisation is created
@receiver(post_save, sender=Organisation)
def create_organisation_group(sender, instance, created, **kwargs):
    if created:
        # Create a Group with the same name as the organisation
        Group.objects.get_or_create(name=instance.name)
        print(f"Group '{instance.name}' created.")