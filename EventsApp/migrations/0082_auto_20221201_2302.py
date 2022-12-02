# Generated by Django 3.2.12 on 2022-12-02 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0081_events_positioninfo_datetimes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='scope',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='client',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='geographical_scope',
            field=models.CharField(blank=True, choices=[('National', 'National'), ('Local', 'Local'), ('Provincial', 'Provincial')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='master_table',
            name='registration_type',
            field=models.CharField(blank=True, choices=[('Drop-in', 'Drop-in'), ('Registration', 'Registration')], default='Drop-in', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
