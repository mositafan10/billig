# Generated by Django 3.0.5 on 2020-11-30 18:25

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('not_seen', models.PositiveIntegerField(default=0)),
                ('slug', models.CharField(db_index=True, default=core.utils.generate_slug, editable=False, max_length=8, primary_key=True, serialize=False, unique=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Massage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('picture', models.FileField(blank=True, null=True, upload_to='images/chat/%Y/%m')),
                ('first_day', models.BooleanField(default=False)),
                ('is_seen', models.BooleanField(default=False)),
                ('type_text', models.IntegerField(choices=[(0, 'p2p'), (1, 'admin')], default=0)),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Conversation')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='massage', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
