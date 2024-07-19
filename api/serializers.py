from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField('get_likes')
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'likes', 'comments', 'published_date']

    @classmethod
    def get_likes(self, obj):
        likes = Like.objects.filter(post=obj).count()
        return likes
    
    @classmethod
    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj).values('author', 'text')
        return comments 

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'