# Generated by Django 3.0.5 on 2020-07-11 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20200711_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatid',
            name='chat_id',
            field=models.CharField(default='518127', editable=False, max_length=8, unique=True),
        ),
    ]
