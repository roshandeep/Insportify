# Generated by Django 3.2.8 on 2022-01-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0006_auto_20220114_0217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master_table',
            name='position_price',
        ),
        migrations.AlterField(
            model_name='master_table',
            name='datetimes',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]