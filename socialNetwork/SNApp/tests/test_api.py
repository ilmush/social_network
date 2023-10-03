import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from SNApp.models import Profile
from SNApp.models import Post
from SNApp.serializers import ProfileSerializer


class UserApiTestCase(APITestCase):
    def setUp(self):
        self.user_1 = Profile.objects.create(slug='user1', description='ilmuhayat')
        self.user_2 = Profile.objects.create(slug='user2', description='lalala')
        self.user_3 = Profile.objects.create(slug='user3', description='lalala')

    def test_get(self):
        url = reverse('profile-list')
        response = self.client.get(url)
        serializer_data = ProfileSerializer([self.user_1, self.user_2, self.user_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Profile.objects.all().count())
        url = reverse('profile-list')
        data = {
            'slug': 'user4',
            'description': 'qwerty'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Profile.objects.all().count())
        print(Profile.objects.last().owner)

    def test_update(self):
        url = reverse('profile-detail', args=(self.user_1.slug,))
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


class PostApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.post = Post.objects.create(slug='1', title='title')

    def test_create(self):
        url = reverse('post-list')
        data = {
            'slug': '1',
            'title': 'title'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        print(Post.objects.last().owner)
