from django.contrib.auth.models import User as AuthUser
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(AuthUser, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=15, unique=True)
    image = models.ImageField(blank=True)
    description = models.CharField(max_length=255, blank=True)
    posts = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    followers = models.ManyToManyField(
        'self', through='Follow',
        related_name='followers_user',
        symmetrical=False, blank=True)

    def follow(self, user):
        Follow.objects.get_or_create(follower=self, following=user)

    def unfollow(self, user):
        Follow.objects.filter(follower=self, following=user).delete()

    def is_following(self, user):
        return self.following.filter(id=user.id).exists()

    def is_followed_by(self, user):
        return self.followers.filter(id=user.id).exists()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    owner = models.ForeignKey(AuthUser, related_name="author", on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=15, unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True)
    views = models.ManyToManyField(AuthUser, related_name="post_views", through='UserPostRelation')
    comments = models.ManyToManyField('Comment', related_name="comments", blank=True)

    def __str__(self):
        return self.title


class Follow(models.Model):
    follower = models.ForeignKey(AuthUser, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(AuthUser, related_name='follower_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} подписан на {self.following}'


class UserPostRelation(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_notes = models.BooleanField(default=False)

    def __str__(self):
        return f'Пользователь {self.user} и пост {self.post}'


class Comment(models.Model):
    owner = models.ForeignKey(AuthUser, related_name="author_comment", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=15, unique=True)
    post = models.ForeignKey(Post, related_name="post", on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_created=True)
    likes = models.ManyToManyField(AuthUser, related_name="likes_post", through='UserCommentRelation')

    def __str__(self):
        return f'Комментарий {self.owner} к посту {self.post}'


class UserCommentRelation(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'Пользователь {self.user} отреагировал на {self.comment}'

