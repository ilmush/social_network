from rest_framework import serializers

from SNApp.models import User, Post, Comment, Follow, UserPostRelation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('slug', 'description')
        # fields = ('name', 'email', 'id')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ('slug', 'text')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class UserPostRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = '__all__'

