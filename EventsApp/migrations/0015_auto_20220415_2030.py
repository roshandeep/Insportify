# Generated by Django 3.2.12 on 2022-04-16 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0014_delete_issportsmaster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iseventsmaster',
            name='em_created_by',
        ),
        migrations.RemoveField(
            model_name='iseventsmaster',
            name='em_created_date',
        ),
        migrations.RemoveField(
            model_name='iseventsmaster',
            name='em_desc',
        ),
        migrations.RemoveField(
            model_name='iseventsmaster',
            name='em_fk_etm_id',
        ),
        migrations.RemoveField(
            model_name='iseventsmaster',
            name='em_gender',
        ),
        migrations.RemoveField(
            model_name='iseventsmaster',
            name='em_id',
        ),
        migrations.RemoveField(
            model_name='iseventsmaster',
            name='em_isactive',
        ),
        migrations.RemoveField(
            model_name='iseventsmaster',
            name='em_updated_by',
        ),
        migrations.RemoveField(
            model_name='iseventsmaster',
            name='em_updated_date',
        ),
    ]
