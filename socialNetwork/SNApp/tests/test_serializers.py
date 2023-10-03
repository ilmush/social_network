from django.test import TestCase

from SNApp.models import Profile
from SNApp.serializers import ProfileSerializer


class UserSerializerTestCase(TestCase):
    def test_ok(self):
        user_1 = Profile.objects.create(slug='user1', description='ilmuhayat')
        user_2 = Profile.objects.create(slug='user2', description='lalala')
        data = ProfileSerializer([user_1, user_2], many=True).data
        expected_data = [
            {
                'slug': user_1.slug,
                'description': 'ilmuhayat'
            },
            {
                'slug': user_2.slug,
                'description': 'lalala'
            },
        ]
        self.assertEqual(expected_data, data)
