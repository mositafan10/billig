# Generated by Django 3.0.5 on 2020-10-11 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0044_auto_20201009_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='status',
            field=models.IntegerField(choices=[(0, 'در انتظار تایید'), (1, 'عدم تایید'), (2, 'منتشر شده'), (3, 'دارای بسته'), (4, 'انجام شده'), (5, 'حذف شده'), (6, 'تسویه شده'), (7, 'تسویه نشده')], default=0),
        ),
    ]
