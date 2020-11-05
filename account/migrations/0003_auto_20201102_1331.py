# Generated by Django 3.0.5 on 2020-11-02 10:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_account_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_number',
            field=models.CharField(blank=True, max_length=24, null=True, validators=[django.core.validators.RegexValidator(message='شماره شبا نامعتبر است', regex='^\\d{1,24}$'), django.core.validators.RegexValidator(message='شماره شبا می\u200cبایست ۲۴ رقم باشد', regex='^.{24}$')]),
        ),
    ]
