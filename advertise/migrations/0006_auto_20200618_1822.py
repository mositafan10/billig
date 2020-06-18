# Generated by Django 3.0.5 on 2020-06-18 13:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertise', '0005_auto_20200617_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packet',
            name='category',
            field=models.CharField(choices=[('0', 'مدرک'), ('1', 'کتاب'), ('2', 'سایر موارد')], max_length=20),
        ),
        migrations.AlterField(
            model_name='travel',
            name='empty_weight',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='travel',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
