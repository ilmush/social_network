from django.contrib.auth.models import User
from django.test import TestCase

from SNApp.models import Profile, Post, Comment, Follow, UserPostRelation, UserCommentRelation
from SNApp.serializers import ProfileSerializer, PostSerializer, CommentSerializer, FollowSerializer, \
    UserPostRelationSerializer, UserCommentRelationSerializer


class ProfileSerializerTestCase(TestCase):
    def setUp(self):
        self.profile_1 = Profile.objects.create(slug='profile1', description='ilmuhayat')
        self.profile_2 = Profile.objects.create(slug='profile2', description='lalala')

    def test_ok(self):
        data = ProfileSerializer([self.profile_1, self.profile_2], many=True).data
        expected_data = [
            {
                'id': self.profile_1.id,
                'user': None,
                'slug': self.profile_1.slug,
                'image': None,
                'description': 'ilmuhayat',
                'posts': None,
            },
            {
                'id': self.profile_2.id,
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
        self.user = User.objects.create(username='user')
        self.user2 = User.objects.create(username='user2')

        self.post_1 = Post.objects.create(owner=self.user, slug='post1', title='title1', description='test')
        self.post_2 = Post.objects.create(owner=self.user, slug='post2', title='title2', description='test')

        UserPostRelation.objects.create(user=self.user, post=self.post_1, like=True)
        UserPostRelation.objects.create(user=self.user2, post=self.post_1, like=True)

        UserPostRelation.objects.create(user=self.user, post=self.post_2, like=True)

    def test_ok(self):
        data = PostSerializer([self.post_1, self.post_2], many=True).data
        expected_data = [
            {
                'id': self.post_1.id,
                'slug': 'post1',
                'title': 'title1',
                'description': 'test',
                'image': None,
                'owner': self.user.id,
                # 'views': [],
                'comments': [],
                'likes_count': 2
            },
            {
                'id': self.post_2.id,
                'slug': 'post2',
                'title': 'title2',
                'description': 'test',
                'image': None,
                'owner': self.user.id,
                # 'views': [],
                'comments': [],
                'likes_count': 1
            },
        ]
        self.assertEqual(expected_data, data)


class CommentSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.user2 = User.objects.create(username='user2')
        self.post = Post.objects.create(slug='post', title='title')
        self.comment_1 = Comment.objects.create(owner=self.user, slug='1', post=self.post, text='text',
                                                created_at='2023-10-04T15:02:00Z')
        self.comment_2 = Comment.objects.create(owner=self.user, slug='2', post=self.post, text='text',
                                                created_at='2023-10-04T15:02:00Z')

        UserCommentRelation.objects.create(user=self.user, comment=self.comment_1, like=True)
        UserCommentRelation.objects.create(user=self.user2, comment=self.comment_1, like=True)

        UserCommentRelation.objects.create(user=self.user, comment=self.comment_2, like=True)

    def test_ok(self):
        data = CommentSerializer([self.comment_1, self.comment_2], many=True).data
        expected_data = [
            {
                'id': self.comment_1.id,
                'created_at': '2023-10-04T15:02:00Z',
                'slug': '1',
                'text': 'text',
                'owner': self.user.id,
                'post': self.post.id,
                # 'likes': [],
                'likes_count': 2,
            },
            {
                'id': self.comment_2.id,
                'created_at': '2023-10-04T15:02:00Z',
                'slug': '2',
                'text': 'text',
                'owner': self.user.id,
                'post': self.post.id,
                # 'likes': [],
                'likes_count': 1,
            },
        ]
        self.assertEqual(expected_data, data)


class FollowSerializerTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='user1')
        self.user_2 = User.objects.create(username='user2')
        self.follow = Follow.objects.create(follower=self.user_1, following=self.user_2,
                                            created_at='2023-10-05T18:49:52.263701Z')

    def test_ok(self):
        data = FollowSerializer(self.follow).data
        expected_data = {
            'id': self.follow.id,
            'created_at': '2023-10-05T18:49:52.263701Z',
            'follower': self.user_1.id,
            'following': self.user_2.id
            }
        self.assertEqual(expected_data, data)


class UserPostRelationSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.post = Post.objects.create(slug='post', title='title')
        self.relation = UserPostRelation.objects.create(user=self.user, post=self.post, like=False, in_notes=False)

    def test_ok(self):
        data = UserPostRelationSerializer(self.relation).data
        expected_data = {
            'like': False,
            'in_notes': False,
            'user': self.user.id,
            'post': self.post.id
        }
        self.assertEqual(expected_data, data)


class UserCommentRelationSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.post = Post.objects.create(slug='post', title='title')
        self.comment = Comment.objects.create(owner=self.user, slug='1', post=self.post, text='text',
                                              created_at='2023-10-04T15:02:00Z')
        self.relation = UserCommentRelation.objects.create(user=self.user, comment=self.comment, like=True)

    def test_ok(self):
        data = UserCommentRelationSerializer(self.relation).data
        expected_data = {
            'like': True,
            'user': self.user.id,
            'comment': self.comment.id
        }
        self.assertEqual(expected_data, data)
