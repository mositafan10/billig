from django.contrib import admin
from .models import Massage, Conversation


class MassageAdmin(admin.ModelAdmin):
    list_display = ('id','owner','chat_id','text','picture','create_at')
   
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id','sender', 'receiver','offer','offer_state','create_at','updated_at')

admin.site.register(Massage,MassageAdmin)
admin.site.register(Conversation,ConversationAdmin)

