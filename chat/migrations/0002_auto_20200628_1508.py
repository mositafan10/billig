# Generated by Django 3.0.5 on 2020-06-28 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='massage',
            name='mtype',
        ),
        migrations.AlterField(
            model_name='massage',
            name='chat_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]