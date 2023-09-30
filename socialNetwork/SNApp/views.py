from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.viewsets import ReadOnlyModelViewSet

from SNApp.models import User, Post, Comment, Follow, UserPostRelation
from SNApp.serializers import UserSerializer, PostSerializer, CommentSerializer, FollowSerializer, \
    UserPostRelationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'slug'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['views']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['likes']


class FollowViewSet(ReadOnlyModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class UserPostRelationViewSet(ReadOnlyModelViewSet):
    queryset = UserPostRelation.objects.all()
    serializer_class = UserPostRelationSerializer

