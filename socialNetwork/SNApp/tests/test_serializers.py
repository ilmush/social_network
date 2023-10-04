from django.contrib.auth.models import User
from django.test import TestCase

from SNApp.models import Profile, Post, Comment
from SNApp.serializers import ProfileSerializer, PostSerializer, CommentSerializer


class ProfileSerializerTestCase(TestCase):
    def setUp(self):
        self.profile_1 = Profile.objects.create(slug='profile1', description='ilmuhayat')
        self.profile_2 = Profile.objects.create(slug='profile2', description='lalala')

    def test_ok(self):
        data = ProfileSerializer([self.profile_1, self.profile_2], many=True).data
        expected_data = [
            {
                'user': None,
                'slug': self.profile_1.slug,
                'image': None,
                'description': 'ilmuhayat',
                'posts': None,
                'followers': None
            },
            {
                'user': None,
                'slug': self.profile_1.slug,
                'image': None,
                'description': 'lalala',
                'posts': None,
                'followers': None
            },
        ]


class PostSerializerTestCase(TestCase):
    def setUp(self):
        self.post_1 = Post.objects.create(slug='post1', title='title1', description='test')
        self.post_2 = Post.objects.create(slug='post2', title='title2', description='test')

    def test_ok(self):
        data = PostSerializer([self.post_1, self.post_2], many=True).data
        expected_data = [
            {
                'owner': None,
                'slug': self.post_2.slug,
                'title': 'title1',
                'description': 'test',
                'image': None,
                'views': None,
                'comments': None
            },
            {
                'owner': None,
                'slug': self.post_2.slug,
                'title': 'title2',
                'description': 'test',
                'image': None,
                'views': None,
                'comments': None
            },
        ]


class CommentSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.post = Post.objects.create(slug='post', title='title')
        self.comment_1 = Comment.objects.create(owner=self.user, slug='1', post=self.post, text='text', created_at='2023-10-04T15:02:00Z')

    def test_ok(self):
        data = CommentSerializer(self.comment_1).data
        expected_data = [
            {
                'owner': self.comment_1.owner,
                'slug': '1',
                'post': self.comment_1.post,
                'text': 'text',
                'created_at': '2023-10-04T15:02:00Z',
            }
        ]
