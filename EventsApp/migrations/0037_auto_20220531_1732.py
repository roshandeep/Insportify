# Generated by Django 3.2.12 on 2022-05-31 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0036_remove_eventsappmastertable_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventsappmastertable',
            name='max_age',
        ),
        migrations.RemoveField(
            model_name='eventsappmastertable',
            name='min_age',
        ),
        migrations.RemoveField(
            model_name='eventsappmastertable',
            name='no_of_position',
        ),
        migrations.RemoveField(
            model_name='eventsappmastertable',
            name='position_cost',
        ),
    ]
