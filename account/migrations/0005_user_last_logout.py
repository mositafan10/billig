# Generated by Django 3.0.5 on 2020-08-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200819_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_logout',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last logout'),
        ),
    ]