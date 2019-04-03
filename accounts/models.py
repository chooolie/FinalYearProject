from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from accounts.choices import *

class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().all()
        #creating filters for searching in manage.py shell
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    Gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    Age = models.CharField(choices=AGE_CHOICES, max_length=20)
    Occupation = models.CharField(choices=JOB_CHOICES, max_length=20)
    dublin = UserProfileManager()
    objects = models.Manager()



def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user = kwargs['instance'])

post_save.connect(create_profile, sender=User)
