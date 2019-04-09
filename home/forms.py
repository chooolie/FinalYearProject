from django import forms
from home.models import Post

class HomeForm(forms.ModelForm):
    movie_name = forms.CharField(widget = forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Movie name',
        }
    ))
    post = forms.CharField(widget = forms.Textarea(
        attrs={
            'class':'form-control',
            'placeholder': 'Write a review',
        }
    ))

    class Meta:
        model = Post
        fields = ('movie_name','post',)
