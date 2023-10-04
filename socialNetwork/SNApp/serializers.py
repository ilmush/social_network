from rest_framework import serializers

from SNApp.models import Profile, Post, Comment, Follow, UserPostRelation


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ('owner', 'post', 'created_at', 'likes')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class UserPostRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = '__all__'

