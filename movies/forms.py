from django import forms
from django.contrib.auth.models import User
from accounts.choices import *
from .models import *
from django.utils.translation import ugettext_lazy as _

class RatingForm(forms.ModelForm):
	rating =  models.FloatField(choices=RATING_CHOICE,default = 2.5)
	class Meta:
		model = UserRatings
		fields = ('rating',)
		labels = {
            "rating": _(""),
        }

class CreateGroup(forms.ModelForm):
	group_name = models.CharField(max_length=50)
	class Meta:
		model = GroupInfo
		fields = ('group_name',)

class AddMovieToGroup(forms.ModelForm):
	#group = models.CharField(choices=GroupInfo.objects.all())
	#group = models.CharField(choices = GroupInfo._meta.get_field('group_name').choices)
	group = models.CharField( choices = GroupInfo.objects.all().values_list('group_name', flat=True) )
	#group = forms.ModelChoiceField(queryset=GroupInfo.filter(taken=False))
	class Meta:
		model = GroupMovieList
		fields = ('group',)
		labels = {
            "group": _("Select Group"),
        }

#MyModel._meta.get_field('foo').choices
'''
class JoinGroup(forms.ModelForm):
	class Meta:
		model = GroupUsers
		fields = (,)
'''
