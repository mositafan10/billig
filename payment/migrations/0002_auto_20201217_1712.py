# Generated by Django 3.0.5 on 2020-12-17 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0004_auto_20201216_0642'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionsend',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='transactionreceive',
            name='packet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packet', to='advertise.Packet'),
        ),
    ]
