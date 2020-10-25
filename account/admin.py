from django.contrib import admin
from .models import Profile, Score, User, Newsletter, Social

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone_number', 'last_login', 'last_logout')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','country','city')
    list_filter = ('country','city')


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('owner','reciever','text','score','create_at')
    list_filter = ('score',)
    search_fields = ('owner', 'reciever')

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email',)

class SocialAdmin(admin.ModelAdmin):
    list_display = ('profile', 'address', 'account_type')


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Social, SocialAdmin)
