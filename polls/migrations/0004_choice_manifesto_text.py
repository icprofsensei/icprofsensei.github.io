# Generated by Django 5.1.1 on 2024-10-13 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='manifesto_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
