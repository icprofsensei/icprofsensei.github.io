from django.db import migrations
from datetime import date

def set_default_dob(apps, schema_editor):
    UserProfile = apps.get_model('register', 'UserProfile')
    UserProfile.objects.filter(date_of_birth__isnull=True).update(date_of_birth=date(1994, 1, 1))

class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_userprofile_date_of_birth'),  # Ensure it points to the previous migration
    ]

    operations = [
        migrations.RunPython(set_default_dob),
    ]