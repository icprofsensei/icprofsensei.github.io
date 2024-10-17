# your_app/management/commands/create_users_profile.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from register.models import UserProfile  # Make sure to import your UserProfile model

class Command(BaseCommand):
    help = 'Get or create UserProfiles for all users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                self.stdout.write(self.style.SUCCESS(f'UserProfile for {user.username} created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'UserProfile for {user.username} already exists.'))
