# Generated by Django 3.0.5 on 2020-09-17 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0040_auto_20200916_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='advertise',
        ),
        migrations.RemoveField(
            model_name='bookmark',
            name='travel',
        ),
        migrations.AddField(
            model_name='bookmark',
            name='packet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='advertise.Packet'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='packet',
            name='picture',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]