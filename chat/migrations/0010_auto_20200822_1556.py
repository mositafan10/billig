# Generated by Django 3.0.5 on 2020-08-22 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20200822_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='new_massage_receiver',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='new_massage_sender',
        ),
    ]