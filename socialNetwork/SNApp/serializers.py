from rest_framework import serializers

from SNApp.models import Profile, Post, Comment, Follow, UserPostRelation


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # fields = ('image', 'posts', 'followers')
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ('slug', 'title')
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

