from django.contrib import admin
from .models import Post, Category, Comment, Tag, Score, Bookmark

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','category', 'get_tags', 'view_count', 'comment', 'like_count', 'dislike_count','score','score_count', 'is_approved', 'create_at')
    list_editable = ('is_approved',)
    # search_fields = ()

    def get_tags(self,obj):
        # return ','self.tags.all()
        return list(obj.tags.values_list('title', flat=True))  
    get_tags.short_description  = "tags" 
    
    def category(self,obj):
        return obj.category.title
    
    def comment(self,obj):
        return obj.posts.filter(is_approved=True).count()
    comment.short_description  = "comment" 
  
      
class TagAdmin(admin.ModelAdmin):
    list_display = ('__str__','count')

    def count(self,obj):
        return obj.posts.count()

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','parent','count','create_at')
    search_fields = ('title',)

    def count(self,obj):
        return obj.posts.count()
    
    def parent(self,obj):
        return obj.parent

class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__','text','is_approved','create_at')
    search_fields = ('text',)
    list_filter = ('create_at',)
    list_editable = ('is_approved',)

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__','value')
    list_filter = ('value',)

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post','create_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Score, ScoreAdmin)  
admin.site.register(Bookmark, BookmarkAdmin)  