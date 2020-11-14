from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Massage, Conversation

@register(Massage)
class MassageAdmin(admin.ModelAdmin):
    list_display = ('owner','chat_id','text','picture','create_at')
   

@register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('slug','sender', 'receiver','offer','offer_state','create_at','updated_at')

