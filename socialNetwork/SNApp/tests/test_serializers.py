from django.test import TestCase

from SNApp.models import Profile, Post
from SNApp.serializers import ProfileSerializer, PostSerializer


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
