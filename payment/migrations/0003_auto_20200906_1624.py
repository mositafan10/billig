# Generated by Django 3.0.5 on 2020-09-06 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20200906_0626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionreceive',
            old_name='transID',
            new_name='transId',
        ),
    ]
