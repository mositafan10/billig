from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import TransactionReceive, TransactionSend, Bank


@register(TransactionReceive)
class TransactionReceiveAdmin(admin.ModelAdmin):
    list_display = ('id','user','offer','amount','transId','factorNumber','create_at')


@register(TransactionSend)
class TransactionSendAdmin(admin.ModelAdmin):
    list_display = ('id','user','offer','amount','status','transaction_id','create_at')
    list_editable = ('status',)


@register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id','slug','user','name','number','is_active')
    list_editable = ('is_active',)

