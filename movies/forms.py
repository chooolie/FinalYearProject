from django import forms
from django.contrib.auth.models import User
from accounts.choices import *
from .models import *


class RatingForm(forms.ModelForm):
	rating =  models.FloatField(choices=RATING_CHOICE,default = 2.5)
	class Meta:
		model = UserRatings
		fields = ('rating',)
