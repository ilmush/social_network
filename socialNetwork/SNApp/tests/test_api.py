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

