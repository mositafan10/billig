# Generated by Django 3.0.5 on 2020-08-24 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_auto_20200822_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='massage',
            name='first_day',
            field=models.BooleanField(default=False),
        ),
    ]