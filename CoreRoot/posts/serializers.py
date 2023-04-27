from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.serializers import AbstractSerializer
from .models import *


from accounts.serializers import UserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='public_id')
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()


    def get_liked(self, instance):
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False
        return instance.has_liked_by(request.user)
    
    def get_likes_count(self, instance):
        return instance.posts_liked.count()


    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")
        return value

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True

        instance = super().update(instance, validated_data)



    
    

    def to_representation(self, instance):
        print(instance)
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data

        return rep
    

    
        
    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'edited', 'liked' ,  'likes_count' ,   'created', 'updated']
        read_only_fields = ["edited"]


class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='public_id')
    post = serializers.SlugRelatedField(
        queryset=Post.objects.all(), slug_field='public_id')
    
    def validate_post(self, value):
        if self.instance:
            return self.instance.post
        return value


    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance,
                                    validated_data)
        return instance


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data
        return rep
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'body', 'edited',
                    'created', 'updated']
        read_only_fields = ["edited"]