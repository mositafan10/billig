from django.contrib import admin
from .models import Profile, Score, User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone_number', 'last_login', 'last_logout')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','country','city')
    list_filter = ('country','city')


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('owner','reciever','text','score','create_at')
    list_filter = ('score',)
    search_fields = ('owner', 'reciever')


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Score, ScoreAdmin)
