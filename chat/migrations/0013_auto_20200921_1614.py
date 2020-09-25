# Generated by Django 3.0.5 on 2020-09-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_auto_20200903_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='massage',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='images/chat/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='massage',
            name='text',
            field=models.TextField(default=''),
        ),
    ]