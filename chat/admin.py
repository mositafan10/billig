from django.contrib import admin
from .models import Massage


class ChatAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver','text','create_at')
    search_fields = ('sender__username','receiver__username','text')

admin.site.register(Massage,ChatAdmin)

