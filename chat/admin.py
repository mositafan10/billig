from django.contrib import admin
from .models import Massage, ChatID


class MassageAdmin(admin.ModelAdmin):
    list_display = ('chat_id','text','create_at')


class ChatIdAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'chat_id')


admin.site.register(Massage,MassageAdmin)
admin.site.register(ChatID,ChatIdAdmin)

