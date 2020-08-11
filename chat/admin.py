from django.contrib import admin
from .models import Massage, Conversation


class MassageAdmin(admin.ModelAdmin):
    list_display = ('owner','chat_id','text','create_at')
    

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id','sender', 'receiver','offer_state','create_at')

admin.site.register(Massage,MassageAdmin)
admin.site.register(Conversation,ConversationAdmin)

