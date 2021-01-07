# Generated by Django 3.0.5 on 2021-01-02 15:34

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0016_auto_20210102_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyinfo',
            name='slug',
            field=models.CharField(default=core.utils.generate_slug, editable=False, max_length=8, unique=True),
        ),
    ]