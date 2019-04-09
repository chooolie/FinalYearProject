from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    movie_name = models.CharField(max_length=100, default = "Not available")
    post = models.CharField(max_length= 1000)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add = True)
    edited = models.DateTimeField(auto_now = True)

class AddFriend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def adding(cls, current_user, new_user):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_user)

    @classmethod
    def deleting(cls, current_user, new_user):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_user)
