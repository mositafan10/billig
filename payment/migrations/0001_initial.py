# Generated by Django 3.0.5 on 2020-10-17 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionSend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField()),
                ('status', models.IntegerField(choices=[(0, 'در انتظار تایید'), (1, 'تایید پرداخت'), (2, 'انجام شده'), (3, 'انجام نشده')], default=0)),
                ('travel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travel', to='advertise.Travel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_travel', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionReceive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('transId', models.BigIntegerField()),
                ('amount', models.FloatField()),
                ('status', models.BooleanField()),
                ('factorNumber', models.IntegerField()),
                ('packet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travel', to='advertise.Packet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_packet', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
