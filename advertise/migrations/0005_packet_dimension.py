# Generated by Django 3.0.5 on 2020-08-15 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0004_auto_20200815_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='packet',
            name='dimension',
            field=models.IntegerField(choices=[(0, 'کوچک'), (1, 'متوسط'), (2, 'بزرگ')], default=0),
            preserve_default=False,
        ),
    ]