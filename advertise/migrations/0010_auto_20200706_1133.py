# Generated by Django 3.0.5 on 2020-07-06 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0009_auto_20200706_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='flight_date_start',
            field=models.CharField(max_length=12),
        ),
    ]
