# Generated by Django 3.0.5 on 2020-12-17 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0004_auto_20201216_0642'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='offer_type',
            field=models.CharField(choices=[(0, 'مسافر'), (1, 'خرید'), (2, 'اشتراک')], default=0, max_length=1),
        ),
    ]