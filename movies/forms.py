from django import forms
from django.contrib.auth.models import User
from accounts.choices import *
from .models import *


class RatingForm(forms.ModelForm):
	rating =  models.FloatField(choices=RATING_CHOICE,default = 2.5)
	class Meta:
		model = UserRatings
		fields = ('rating',)

class CreateGroup(forms.ModelForm):
	group_name = models.CharField(max_length=50)
	class Meta:
		model = GroupInfo
		fields = ('group_name',)

'''
class JoinGroup(forms.ModelForm):
	class Meta:
		model = GroupUsers
		fields = (,)
'''
