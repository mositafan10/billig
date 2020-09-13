# Generated by Django 3.0.5 on 2020-09-13 07:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0020_auto_20200913_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packet',
            name='weight',
            field=models.DecimalField(decimal_places=0, max_digits=3, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)]),
        ),
    ]
