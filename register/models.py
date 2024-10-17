
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from Organisations.models import Organisation
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

