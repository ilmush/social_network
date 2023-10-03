import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from SNApp.models import Profile
from SNApp.models import Post
from SNApp.serializers import ProfileSerializer, PostSerializer


class UserApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.profile_1 = Profile.objects.create(slug='profile1', description='ilmuhayat')
        self.profile_2 = Profile.objects.create(slug='profile2', description='lalala')
        self.profile_3 = Profile.objects.create(slug='profile3', description='lalala')

    def test_get(self):
        url = reverse('profile-list')
        response = self.client.get(url)
        serializer_data = ProfileSerializer([self.profile_1, self.profile_2, self.profile_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Profile.objects.all().count())
        url = reverse('profile-list')
        data = {
            'slug': 'profile4',
            'description': 'qwerty'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Profile.objects.all().count())
        print(Profile.objects.last().user)

    def test_update(self):
        url = reverse('profile-detail', args=(self.profile_1.slug,))
        data = {
            'slug': self.profile_1.slug,
            'description': '123'
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.profile_1.refresh_from_db()
        self.assertEqual('123', self.profile_1.description)


class PostApiTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='test')
        self.post_1 = Post.objects.create(slug='1', title='title')
        self.post_2 = Post.objects.create(slug='2', title='title2')

    def test_get(self):
        url = reverse('post-list')
        response = self.client.get(url)
        serializer_data = PostSerializer([self.post_1, self.post_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('post-list')
        data = {
            'slug': '3',
            'title': 'qwerty'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.owner)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Post.objects.all().count())
        print(Post.objects.last().owner)

    def test_update(self):
        url = reverse('post-detail', args=(self.post_1.slug,))
        data = {
            'slug': self.post_1.slug,
            'title': 'title'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.owner)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.post_1.refresh_from_db()
        self.assertEqual('title', self.post_1.title)
