from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from SNApp.models import Profile, Post, Comment, Follow, UserPostRelation
from SNApp.permissions import IsOwnerOrReadOnly
from SNApp.serializers import ProfileSerializer, PostSerializer, CommentSerializer, FollowSerializer, \
    UserPostRelationSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'slug'
    # filter_backends = [DjangoFilterBackend]
    # filter_fields = ['name']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['title']
    ordering_fields = ['views', 'comments']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'slug'
    # permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['likes']

    # def perform_create(self, serializer):
    #     serializer.validated_data['owner'] = self.request.user
    #     serializer.save()


class FollowViewSet(ReadOnlyModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class UserPostRelationViewSet(ReadOnlyModelViewSet):
    queryset = UserPostRelation.objects.all()
    serializer_class = UserPostRelationSerializer

