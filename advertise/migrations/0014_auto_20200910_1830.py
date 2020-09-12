# Generated by Django 3.0.5 on 2020-09-10 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0013_auto_20200908_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packet',
            name='picture',
            field=models.ManyToManyField(blank=True, null=True, related_name='packets', to='advertise.PacketPicture'),
        ),
        migrations.AlterField(
            model_name='packetpicture',
            name='image_file',
            field=models.FileField(upload_to='images/test/%Y/%m'),
        ),
    ]
