from django import forms
from movie.models import UserDemographics

class UserDemographicsForm(forms.ModelForm):
     post = forms.CharField(widget = forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Write a post',
        }
     ))

     class Meta:
         model = Post
         fields = ('post',)
