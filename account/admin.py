from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Profile, Score, User, Newsletter, Social, CommentUser

@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('slug','name','phone_number', 'last_login')


@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','country','city', 'travel_done', 'billlig_done' )
    list_filter = ('country','city')


@register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('owner','reciever','text','score','create_at')
    list_filter = ('score',)
    search_fields = ('owner', 'reciever')


@register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email',)


@register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ('profile', 'address', 'account_type')

@register(CommentUser)
class CommentUserAdmin(admin.ModelAdmin):
    list_display = ('id','slug','owner', 'text','is_approved')
    list_editable = ('is_approved',)
    


