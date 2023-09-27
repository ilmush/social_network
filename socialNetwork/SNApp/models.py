from django.conf import settings
from django.db import models


class User(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    slug = models.SlugField(max_length=15)
    image = models.ImageField()
    description = models.CharField(max_length=255, blank=True)
    posts = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True)
    followers = models.ManyToManyField('self', through='Follow', related_name='followers_user', symmetrical=False, blank=True)

    @property
    def name(self):
        if self.user_id is not None:
            return self.user.username

    @property
    def email(self):
        if self.user_id is not None:
            return self.user.email

    def follow(self, user):
        Follow.objects.get_or_create(follower=self, following=user)

    def unfollow(self, user):
        Follow.objects.filter(follower=self, following=user).delete()

    def is_following(self, user):
        return self.following.filter(id=user.id).exists()

    def is_followed_by(self, user):
        return self.followers.filter(id=user.id).exists()

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey('User', related_name="author", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=15)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField()
    views = models.ManyToManyField('User', related_name="post_views", through='UserPostRelation')
    comments = models.ManyToManyField('Comment', related_name="comments")

    def __str__(self):
        return self.title


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class UserPostRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_notes = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey('User', related_name="author_comment", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=15)
    post = models.ForeignKey('Post', related_name="post", on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_created=True)
