# Generated by Django 3.2.12 on 2022-08-24 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0065_orderitems_purchased'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='purchased',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
