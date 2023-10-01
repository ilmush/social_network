import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from SNApp.models import User
from SNApp.serializers import UserSerializer


class UserApiTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(slug='user1', description='ilmuhayat')
        self.user_2 = User.objects.create(slug='user2', description='lalala')
        self.user_3 = User.objects.create(slug='user3', description='lalala')

    def test_get(self):
        url = reverse('user-list')
        response = self.client.get(url)
        serializer_data = UserSerializer([self.user_1, self.user_2, self.user_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, User.objects.all().count())
        url = reverse('user-list')
        data = {
            'slug': 'user4',
            'description': 'qwerty'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, User.objects.all().count())

    def test_update(self):
        url = reverse('user-detail', args=(self.user_1.slug,))
        data = {
            'slug': self.user_1.slug,
            'description': '123'
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user_1.refresh_from_db()
        self.assertEqual('123', self.user_1.description)
