# Generated by Django 3.0.5 on 2020-11-21 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20201121_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='name',
            field=models.CharField(default='mostafa', max_length=30),
            preserve_default=False,
        ),
    ]
