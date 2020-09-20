# Generated by Django 3.0.5 on 2020-09-08 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0012_auto_20200907_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.IntegerField(choices=[(0, 'در انتظار پاسخ'), (1, 'در انتظار تایید مسافر'), (2, 'در انتظار پرداخت'), (3, 'در انتظار خرید'), (4, 'در انتظار تحویل'), (5, 'در انتظار تایید خریدار'), (6, 'انجام شده'), (7, 'تمام شده'), (8, 'حذف شده')], default=0),
        ),
        migrations.AlterField(
            model_name='packet',
            name='status',
            field=models.IntegerField(choices=[(0, 'منتشر شده'), (1, 'دارای پیشنهاد'), (2, 'در انتظار پرداخت'), (3, 'در انتظار خرید'), (4, 'در انتظار تحویل'), (5, 'در انتظار تایید خریدار'), (6, 'انجام شده'), (7, 'تمام شده'), (8, 'حذف شده'), (9, 'منقضی شده'), (10, 'در انتظار تایید'), (11, 'عدم تایید')], default=10),
        ),
    ]