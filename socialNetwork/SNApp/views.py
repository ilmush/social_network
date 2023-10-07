from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from SNApp.models import Profile, Post, Comment, Follow, UserPostRelation, UserCommentRelation
from SNApp.permissions import IsOwnerOrReadOnly
from SNApp.serializers import ProfileSerializer, PostSerializer, CommentSerializer, FollowSerializer, \
    UserPostRelationSerializer, UserCommentRelationSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, ]
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
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['likes']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class FollowViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class UserPostRelationViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserPostRelation.objects.all()
    serializer_class = UserPostRelationSerializer
    lookup_field = 'user'

    def get_object(self):
        obj, _ = UserPostRelation.objects.get_or_create(user=self.request.user,
                                                        post_id=self.kwargs['user'])
        return obj


class UserCommentRelationViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserCommentRelation.objects.all()
    serializer_class = UserCommentRelationSerializer
    lookup_field = 'user'

    def get_object(self):
        obj, _ = UserCommentRelation.objects.get_or_create(user=self.request.user,
                                                           comment_id=self.kwargs['user'])
        return obj
