# Generated by Django 3.0.5 on 2020-09-03 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0010_auto_20200903_2049'),
        ('chat', '0011_massage_first_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer', to='advertise.Offer'),
        ),
    ]