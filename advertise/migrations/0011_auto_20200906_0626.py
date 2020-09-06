# Generated by Django 3.0.5 on 2020-09-06 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0010_auto_20200903_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.IntegerField(choices=[(0, 'در انتظار پاسخ'), (1, 'تایید'), (2, 'عدم تایید'), (3, 'نهایی\u200cشدن مبلغ'), (4, 'تایید مبلغ'), (5, 'حذف شده')], default=0),
        ),
        migrations.AlterField(
            model_name='packet',
            name='category',
            field=models.IntegerField(choices=[(0, 'مدارک و مستندات'), (1, 'کتاب و مجله'), (2, 'لوازم الکترونیکی'), (3, 'کفش و پوشاک'), (4, 'لوازم آرایشی و بهداشتی'), (5, 'دارو'), (6, 'سایر موارد')]),
        ),
        migrations.AlterField(
            model_name='packet',
            name='status',
            field=models.IntegerField(choices=[(0, 'در انتظار تایید'), (1, 'عدم تایید'), (2, 'منتشر شده'), (3, 'دارای پیشنهاد'), (4, 'منقضی شده'), (5, 'حذف شده'), (6, 'در انتظار پرداخت'), (7, 'در حال انجام'), (8, 'انجام شده')], default=0),
        ),
        migrations.AlterField(
            model_name='travel',
            name='status',
            field=models.IntegerField(choices=[(0, 'در انتظار تایید'), (1, 'عدم تایید'), (2, 'منتشر شده'), (3, 'دارای بسته'), (4, 'انجام شده'), (5, 'حذف شده'), (6, 'تسویه شده')], default=0),
        ),
    ]
