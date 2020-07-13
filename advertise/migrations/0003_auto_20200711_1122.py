# Generated by Django 3.0.5 on 2020-07-11 06:52

import advertise.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0002_auto_20200707_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='slug',
            field=models.CharField(default=advertise.utils.generate_slug, editable=False, max_length=8, unique=True),
        ),
    ]
