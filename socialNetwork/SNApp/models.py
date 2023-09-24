from django.conf import settings
from django.db import models


class User(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image = models.ImageField()
    description = models.CharField(max_length=255, blank=True)
    posts = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True)

    @property
    def name(self):
        if self.user_id is not None:
            return self.user.username

    @property
    def email(self):
        if self.user_id is not None:
            return self.user.email

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField()

    def __str__(self):
        return self.title


