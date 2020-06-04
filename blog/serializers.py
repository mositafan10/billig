from rest_framework import serializers
from .models import Post, Category, Tag, Comment, Score


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author','category','tags','pic','text','score','view_post','like_count','is_approved','create_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title','parent']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title',]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user','post','text','parent','is_approved']

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['user','post','value']
