from django.contrib import admin
from .models import TransactionReceive, TransactionSend

class TransactionReceiveAdmin(admin.ModelAdmin):
    list_display = ('id','user','packet','amount','transId','factorNumber','create_at')

class TransactionSendAdmin(admin.ModelAdmin):
    list_display = ('id','user','travel','amount','status','create_at')
    list_editable = ('status',)

admin.site.register(TransactionReceive,TransactionReceiveAdmin)
admin.site.register(TransactionSend,TransactionSendAdmin)

