from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(Gender = 'F')
        #creating filters for searching in manage.py shell
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    Gender = models.CharField("gender", max_length=5, default="M")
    Age = models.CharField("age", max_length=50, default="18-24")
    Occupation = models.CharField("job", max_length= 100, default="other")
    dublin = UserProfileManager()
    objects = models.Manager()

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user = kwargs['instance'])

post_save.connect(create_profile, sender=User)
