# Generated by Django 3.0.5 on 2020-09-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_transactionreceive_factornumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionreceive',
            name='transId',
            field=models.BigIntegerField(),
        ),
    ]