from django.contrib import admin
from .models import TransactionReceive

class TransactionReceiveAdmin(admin.ModelAdmin):
    list_display = ('id','user','packet','amount','transId','factorNumber','create_at')

admin.site.register(TransactionReceive,TransactionReceiveAdmin)

