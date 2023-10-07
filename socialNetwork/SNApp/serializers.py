from rest_framework import serializers

from SNApp.models import Profile, Post, Comment, Follow, UserPostRelation, UserCommentRelation


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'slug', 'title', 'description', 'image', 'owner', 'comments', 'likes_count')
        # fields = '__all__'

    def get_likes_count(self, instance):
        return UserPostRelation.objects.filter(post=instance, like=True).count()


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'owner', 'slug', 'post', 'text', 'created_at', 'likes_count')

    def get_likes_count(self, instance):
        return UserCommentRelation.objects.filter(comment=instance, like=True).count()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class UserPostRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = ('user', 'post', 'like', 'in_notes')


class UserCommentRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCommentRelation
        fields = ('user', 'comment', 'like')
