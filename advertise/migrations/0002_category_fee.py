# Generated by Django 3.0.5 on 2021-01-12 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='fee',
            field=models.PositiveIntegerField(default=5),
        ),
    ]
