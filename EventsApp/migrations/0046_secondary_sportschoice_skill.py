# Generated by Django 3.2.12 on 2022-07-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0045_remove_secondary_sportschoice_sport_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondary_sportschoice',
            name='skill',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
