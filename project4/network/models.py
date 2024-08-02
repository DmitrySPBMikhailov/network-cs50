from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    have_followers_count = models.PositiveIntegerField("followers", default=0)
    followed_by_user_count = models.PositiveIntegerField("User follows", default=0)


class UserNetwork(models.Model):
    parent = models.ForeignKey(User, related_name='parent_user', on_delete=models.CASCADE)
    child = models.ForeignKey(User, related_name='child_user', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)

    def __str__(self):
        return '{} watches {}'.format(self.parent, self.child)


class Post(models.Model):
    text = models.TextField("Post", null=True, blank=False)
    likes_count = models.PositiveIntegerField("likes", default=0)
    dt = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)
    user_author = models.ForeignKey(User, on_delete=models.CASCADE)
    user_liked_this = models.ManyToManyField(User, verbose_name='User liked post', related_name="user_liked_post", blank=True)

    class Meta:
        ordering = ['-dt']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
