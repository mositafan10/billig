# Generated by Django 3.0.5 on 2020-07-11 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20200711_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatid',
            name='chat_id',
            field=models.CharField(default='332348', editable=False, max_length=8, unique=True),
        ),
    ]
