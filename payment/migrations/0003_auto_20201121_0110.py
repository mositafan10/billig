# Generated by Django 3.0.5 on 2020-11-20 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20201121_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionreceive',
            name='factorNumber',
            field=models.CharField(max_length=8),
        ),
    ]
