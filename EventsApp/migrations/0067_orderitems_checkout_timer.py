# Generated by Django 3.2.12 on 2022-08-29 23:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0066_alter_orderitems_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='checkout_timer',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 8, 29, 19, 37, 9, 499868)),
            preserve_default=False,
        ),
    ]
