# Generated by Django 3.2.12 on 2023-03-23 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0005_alter_user_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='active_profile_name',
        ),
    ]
