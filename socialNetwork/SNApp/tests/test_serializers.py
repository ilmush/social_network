from django.contrib.auth.models import User
from django.test import TestCase

from SNApp.models import Profile, Post, Comment, Follow, UserPostRelation
from SNApp.serializers import ProfileSerializer, PostSerializer, CommentSerializer, FollowSerializer


class ProfileSerializerTestCase(TestCase):
    def setUp(self):
        self.profile_1 = Profile.objects.create(slug='profile1', description='ilmuhayat')
        self.profile_2 = Profile.objects.create(slug='profile2', description='lalala')

    def test_ok(self):
        data = ProfileSerializer([self.profile_1, self.profile_2], many=True).data
        expected_data = [
            {
                'id': 1,
                'user': None,
                'slug': self.profile_1.slug,
                'image': None,
                'description': 'ilmuhayat',
                'posts': None,
            },
            {
                'id': 2,
                'user': None,
                'slug': self.profile_2.slug,
                'image': None,
                'description': 'lalala',
                'posts': None,
            },
            ]

        self.assertEqual(expected_data, data)


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
        self.assertEqual(expected_data, data)


class CommentSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.post = Post.objects.create(slug='post', title='title')
        self.comment = Comment.objects.create(owner=self.user, slug='1', post=self.post, text='text', created_at='2023-10-04T15:02:00Z')

    def test_ok(self):
        data = CommentSerializer(self.comment).data
        expected_data = [
            {
                'owner': 'user',
                'slug': '1',
                'post': self.comment.post,
                'text': 'text',
                'created_at': '2023-10-04T15:02:00Z',
            }
        ]
        self.assertEqual(expected_data, data)


class FollowSerializerTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='user1')
        self.user_2 = User.objects.create(username='user2')
        self.follow = Follow.objects.create(follower=self.user_1, following=self.user_2, created_at='2023-10-04T21:58:00Z')

    def test_ok(self):
        data = FollowSerializer(self.follow).data
        expected_data = [
            {
                'follower': 'user1',
                'following': 'user2',
                'created_at': '2023-10-04T21:58:00Z'
            }
        ]
        self.assertEqual(expected_data, data)


class UserPostRelationSerializerTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='user1')
        self.post = Post.objects.create(slug='post', title='title')
        self.relation = UserPostRelation.objects.create(user=self.user_1, post=self.post, like=False, in_notes=False)

    def test_ok(self):
        data = FollowSerializer(self.follow).data
        expected_data = [
            {
                'user': 'user1',
                'post': 'post',
                'like': False,
                'in_notes': False
            }
        ]
        self.assertEqual(expected_data, data)
