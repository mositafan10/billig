# Generated by Django 3.0.5 on 2020-06-02 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='status',
            field=models.CharField(choices=[('0', 'در انتظار تایید'), ('1', 'عدم تایید'), ('2', 'منتشر شده'), ('3', 'دارای بسته'), ('4', 'پرواز کرد')], default='در انتظار تایید', max_length=30),
        ),
    ]
