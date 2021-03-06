# Generated by Django 3.0.5 on 2021-01-10 20:20

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0005_auto_20201230_0145'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('eng_name', models.CharField(max_length=30)),
                ('picture', models.FileField(upload_to='images/category')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Packet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('no_matter_origin', models.BooleanField(default=False)),
                ('weight', models.IntegerField(choices=[(0, 'کمتر از ۱ کیلوگرم'), (1, 'بین ۱ تا ۵ کیلوگرم'), (2, 'بین ۵ تا ۱۰ کیلوگرم'), (3, 'بیشتر از ۱۰ کیلوگرم')])),
                ('dimension', models.IntegerField(choices=[(0, 'کوچک'), (1, 'متوسط'), (2, 'بزرگ')])),
                ('suggested_price', models.PositiveIntegerField(default=0)),
                ('buy', models.BooleanField(default=False)),
                ('phonenumber_visible', models.BooleanField(default=False)),
                ('picture', models.CharField(default=1, max_length=8)),
                ('visit_count', models.PositiveIntegerField(default=0)),
                ('offer_count', models.PositiveIntegerField(default=0)),
                ('description', models.CharField(max_length=1000)),
                ('slug', models.CharField(default=core.utils.generate_slug, editable=False, max_length=10, unique=True)),
                ('status', models.IntegerField(choices=[(0, 'منتشر شده'), (1, 'دارای پیشنهاد'), (2, 'در انتظار پرداخت'), (3, 'در انتظار خرید'), (4, 'در انتظار تحویل'), (5, 'در انتظار تایید خریدار'), (6, 'انجام شده'), (7, 'تمام شده'), (8, 'حذف شده'), (9, 'منقضی شده'), (10, 'در انتظار تایید'), (11, 'عدم تایید')], default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='advertise.Category')),
                ('destination_city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination_city', to='account.City')),
                ('destination_country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination_country', to='account.Country')),
                ('origin_city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origin_city', to='account.City')),
                ('origin_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origin_country', to='account.Country')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('flight_date_start', models.DateField()),
                ('flight_date_end', models.DateField(blank=True, null=True)),
                ('offer_count', models.PositiveIntegerField(default=0)),
                ('income', models.PositiveIntegerField(default=0)),
                ('approved_packet', models.PositiveIntegerField(default=0)),
                ('slug', models.CharField(default=core.utils.generate_slug, editable=False, max_length=8, unique=True)),
                ('status', models.IntegerField(choices=[(0, 'در انتظار تایید'), (1, 'عدم تایید'), (2, 'منتشر شده'), (3, 'دارای بسته'), (4, 'انجام شده'), (5, 'حذف شده'), (6, 'تسویه شده'), (7, 'تسویه نشده'), (8, 'در انتظار تسویه')], default=2)),
                ('departure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='depar_country', to='account.Country')),
                ('departure_city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='depar_city', to='account.City')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dest_country', to='account.Country')),
                ('destination_city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dest_city', to='account.City')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TravelRemoveReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_remove', models.IntegerField(choices=[(0, 'آگهی مناسبی پیدا نکردم'), (1, 'سفرم کنسل شد'), (2, 'هیچ کدوم از پیشنهاداتم قبول نشد'), (3, 'دستمزدها کم بود'), (4, 'به دلایل دیگر')])),
                ('description', models.TextField(blank=True, null=True)),
                ('travel', models.ForeignKey(on_delete=django.db.models.expressions.Case, to='advertise.Travel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('eng_name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('categoty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertise.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.IntegerField(choices=[(0, 'عدم تطابق آگهی با صحبت\u200cهای بیلیگر'), (1, 'مغایرت محتویات بسته با قوانین'), (2, 'دستمزد نامتعارف'), (3, 'به دلایل دیگر')])),
                ('text', models.TextField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL)),
                ('packet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertise.Packet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RemoveReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_remove', models.IntegerField(choices=[(0, 'بسته از طریق دیگری ارسال شد'), (1, 'پیشنهادی دریافت نکردم'), (2, 'منصرف شدم'), (3, 'به دلایل دیگر')])),
                ('description', models.TextField(blank=True, null=True)),
                ('packet', models.ForeignKey(on_delete=django.db.models.expressions.Case, to='advertise.Packet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PacketPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_file', models.FileField(upload_to='images/%Y/%m')),
                ('slug', models.CharField(default=core.utils.generate_slug, editable=False, max_length=8, unique=True)),
                ('packet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='advertise.Packet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='packet',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='advertise.SubCategory'),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.PositiveIntegerField()),
                ('parcelPrice', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.CharField(default=core.utils.generate_slug, editable=False, max_length=8, unique=True)),
                ('status', models.IntegerField(choices=[(0, 'در انتظار پاسخ'), (1, 'در انتظار تایید مسافر'), (2, 'در انتظار پرداخت'), (3, 'در انتظار خرید'), (4, 'در انتظار تحویل'), (5, 'در انتظار تایید خریدار'), (6, 'انجام شده'), (7, 'تمام شده'), (8, 'حذف شده')], default=0)),
                ('offer_type', models.IntegerField(choices=[(0, 'مسافر'), (1, 'خرید'), (2, 'اشتراک')], default=0)),
                ('packet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packet_ads', to='advertise.Packet')),
                ('travel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travel_ads', to='advertise.Travel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Buyinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('slug', models.CharField(default=core.utils.generate_slug, editable=False, max_length=8, unique=True)),
                ('packet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packet_info', to='advertise.Packet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.CharField(default=core.utils.generate_slug, editable=False, max_length=8, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookmark_owner', to=settings.AUTH_USER_MODEL)),
                ('packet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_packet', to='advertise.Packet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
