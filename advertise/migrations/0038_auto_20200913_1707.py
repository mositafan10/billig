# Generated by Django 3.0.5 on 2020-09-13 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0037_auto_20200913_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packet',
            name='category_other',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]