# Generated by Django 3.0.5 on 2020-09-21 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0041_auto_20200917_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='packet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_packet', to='advertise.Packet'),
        ),
    ]
