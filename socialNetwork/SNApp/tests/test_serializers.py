from django.test import TestCase

from SNApp.models import User
from SNApp.serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def test_ok(self):
        user_1 = User.objects.create(slug='user1', description='ilmuhayat')
        user_2 = User.objects.create(slug='user2', description='lalala')
        data = UserSerializer([user_1, user_2], many=True).data
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
