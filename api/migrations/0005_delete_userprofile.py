# Generated by Django 5.1.4 on 2025-01-10 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_userprofile_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
