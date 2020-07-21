from django.contrib import admin
from .models import Profile, Social, CommentUser, Score, Follow, User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','phone_number')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','country','city')
    list_filter = ('country','city')

class SocialAdmin(admin.ModelAdmin):
    list_display = ('user','title','social_id', 'is_approved')
    list_filter = ('title',)
    search_fields = ('user',)

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('owner','reciever','score','create_at')
    list_filter = ('score',)
    search_fields = ('owner', 'reciever')

class FollowAdmin(admin.ModelAdmin):
    list_display=('follower','following','create_at','status')
    search_fields = ('follower','following')
    list_filter = ('create_at',)

class CommentUserAdmin(admin.ModelAdmin):
    list_display = ('owner','receiver','comment','is_approved','create_at')
    list_filter = ('create_at',)
    # search_fields = ('owner','receiver','comment') with error , why ?



admin.site.register(User, UserAdmin)
admin.site.register(Social, SocialAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CommentUser,CommentUserAdmin)
admin.site.register(Score,ScoreAdmin)
admin.site.register(Follow,FollowAdmin)
