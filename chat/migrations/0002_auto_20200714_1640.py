# Generated by Django 3.0.5 on 2020-07-14 12:10

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='conversation',
            managers=[
                ('chatlist', django.db.models.manager.Manager()),
            ],
        ),
    ]
