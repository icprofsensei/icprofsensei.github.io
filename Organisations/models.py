from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here. Imagine each class as a unique table 

class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Organisation name
    org_admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organisation')  # Associate with a primary user
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the organisation was created

    def __str__(self):
        return self.name