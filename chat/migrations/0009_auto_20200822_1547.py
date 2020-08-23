# Generated by Django 3.0.5 on 2020-08-22 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_conversation_new_massage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversation',
            old_name='new_massage',
            new_name='new_massage_receiver',
        ),
        migrations.AddField(
            model_name='conversation',
            name='new_massage_sender',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
