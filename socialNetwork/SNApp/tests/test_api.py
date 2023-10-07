import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from SNApp.models import Profile, Post, Comment, UserPostRelation, UserCommentRelation
from SNApp.serializers import ProfileSerializer, PostSerializer, CommentSerializer


class ProfileApiTestCase(APITestCase):
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
        self.assertEqual(self.user, Profile.objects.last().user)

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
        self.post_1 = Post.objects.create(slug='1', title='title1', owner=self.owner)
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
        self.assertEqual(self.owner, Post.objects.last().owner)

    def test_update(self):
        url = reverse('post-detail', args=(self.post_1.slug,))
        data = {
            'slug': self.post_1.slug,
            'title': 'otherTitle'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.owner)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.post_1.refresh_from_db()
        self.assertEqual('otherTitle', self.post_1.title)

    def test_update_not_owner(self):
        self.user2 = User.objects.create_user(username='test2')
        url = reverse('post-detail', args=(self.post_1.slug,))
        data = {
            'slug': self.post_1.slug,
            'title': 'otherTitle'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.post_1.refresh_from_db()
        self.assertEqual('title1', self.post_1.title)


class CommentApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.post = Post.objects.create(slug='post', title='title')
        self.comment_1 = Comment.objects.create(owner=self.user, slug='1', post=self.post, text='text',
                                                created_at='2023-10-04T15:02:00Z')
        self.comment_2 = Comment.objects.create(owner=self.user, slug='2', post=self.post, text='text',
                                                created_at='2023-10-04T15:02:00Z')

    def test_get(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        serializer_data = CommentSerializer([self.comment_1, self.comment_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(2, Comment.objects.all().count())
        url = reverse('comment-list')
        data = {
            'owner': self.user.id,
            'slug': '3',
            'post': self.post.id,
            'text': 'text3',
            'created_at': '2023-10-07T00:00:00Z'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Comment.objects.all().count())
        self.assertEqual(self.user, Comment.objects.last().owner)

    def test_update(self):
        url = reverse('comment-detail', args=(self.comment_1.slug,))
        data = {
            'owner': self.user.id,
            'slug': self.comment_1.slug,
            'post': self.post.id,
            'text': 'otherText',
            'created_at': '2023-10-07T00:00:00Z'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.comment_1.refresh_from_db()
        self.assertEqual('otherText', self.comment_1.text)

    def test_update_not_owner(self):
        self.user2 = User.objects.create_user(username='test2')
        url = reverse('comment-detail', args=(self.comment_1.slug,))
        data = {
            'owner': self.user.id,
            'slug': self.comment_1.slug,
            'post': self.post.id,
            'text': 'otherText',
            'created_at': '2023-10-07T00:00:00Z'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.comment_1.refresh_from_db()
        self.assertEqual('text', self.comment_1.text)


class UserPostRelationTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user1')
        self.user2 = User.objects.create(username='test_user2')
        self.post_1 = Post.objects.create(slug='1', title='post1')
        self.post_2 = Post.objects.create(slug='2', title='post2')

    def test_like(self):
        url = reverse('userpostrelation-detail', args=(self.post_1.id,))
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserPostRelation.objects.get(user=self.user1,
                                                post=self.post_1)
        self.assertTrue(relation.like)

        data = {
         'in_notes': True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserPostRelation.objects.get(user=self.user1,
                                                post=self.post_1)
        self.assertTrue(relation.in_notes)


class UserCommentRelationTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user1')
        self.user2 = User.objects.create(username='test_user2')
        self.post = Post.objects.create(slug='post', title='title')
        self.comment_1 = Comment.objects.create(owner=self.user1, slug='1', post=self.post, text='text',
                                                created_at='2023-10-04T15:02:00Z')
        self.comment_2 = Comment.objects.create(owner=self.user2, slug='2', post=self.post, text='text',
                                                created_at='2023-10-04T15:02:00Z')

    def test_like(self):
        url = reverse('usercommentrelation-detail', args=(self.comment_1.id, ))
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserCommentRelation.objects.get(user=self.user1,
                                                   comment=self.comment_1)
        self.assertTrue(relation.like)
