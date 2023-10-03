from django.test import TestCase

from SNApp.models import Profile
from SNApp.serializers import ProfileSerializer


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
