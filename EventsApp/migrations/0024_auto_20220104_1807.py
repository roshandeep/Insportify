# Generated by Django 3.2.8 on 2022-01-04 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0023_auto_20220104_1756'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Todo',
        ),
        migrations.RemoveField(
            model_name='multistep',
            name='ath_max_age',
        ),
        migrations.RemoveField(
            model_name='multistep',
            name='ath_min_age',
        ),
        migrations.RemoveField(
            model_name='multistep',
            name='athelete_level',
        ),
        migrations.RemoveField(
            model_name='multistep',
            name='staff_level',
        ),
        migrations.RemoveField(
            model_name='multistep',
            name='sup_max_age',
        ),
        migrations.RemoveField(
            model_name='multistep',
            name='sup_min_age',
        ),
    ]
