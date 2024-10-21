
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

from Organisations.models import Organisation
class UserProfile(models.Model):
    ETHNICITY_CHOICES = [
        ("Asian", "Asian or Asian British"),
        ("Black", "Black, Black British, Caribbean or African"),
        ("Mixed", "Mixed or multiple ethnic groups"),
        ("White", "White"),
        ("Other", "Other ethnic group"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(
        verbose_name="Birthday",
        default= date(1994, 1, 1),
        null=False
    )
    ethnicity = models.CharField(max_length=50, choices=ETHNICITY_CHOICES, blank=True, null=True)
    def __str__(self):
        return self.user.username

