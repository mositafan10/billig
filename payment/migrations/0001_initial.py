# Generated by Django 3.0.5 on 2021-01-12 20:52

import core.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertise', '0002_category_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('number', models.CharField(blank=True, max_length=24, null=True, validators=[django.core.validators.RegexValidator(message='شماره شبا نامعتبر است', regex='^\\d{1,24}$'), django.core.validators.RegexValidator(message='شماره شبا می\u200cبایست ۲۴ رقم باشد', regex='^.{24}$')])),
                ('slug', models.CharField(default=core.utils.generate_slug, editable=False, max_length=8, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionSend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField()),
                ('transaction_id', models.CharField(blank=True, max_length=15, null=True)),
                ('status', models.IntegerField(choices=[(0, 'در انتظار تایید'), (1, 'تایید پرداخت'), (2, 'انجام شده'), (3, 'انجام نشده')], default=0)),
                ('slug', models.CharField(default=core.utils.generate_slug, editable=False, max_length=8, unique=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.Bank')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_travel', to='advertise.Offer')),
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
                ('factorNumber', models.CharField(max_length=8)),
                ('cardNumber', models.CharField(max_length=16)),
                ('paymentDate', models.CharField(max_length=20)),
                ('slug', models.CharField(default=core.utils.generate_slug, editable=False, max_length=8, unique=True)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_packet', to='advertise.Offer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_packet', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
