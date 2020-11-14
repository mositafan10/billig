from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import TransactionReceive, TransactionSend


@register(TransactionReceive)
class TransactionReceiveAdmin(admin.ModelAdmin):
    list_display = ('id','user','packet','amount','transId','factorNumber','create_at')


@register(TransactionSend)
class TransactionSendAdmin(admin.ModelAdmin):
    list_display = ('id','user','travel','amount','status','create_at')
    list_editable = ('status',)


