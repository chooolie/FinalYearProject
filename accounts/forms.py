from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.choices import *
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
#Used to edit any forms

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        #no sql injection
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

#Get rid of any extra un needed parts of the form
class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
        'first_name',
        'last_name',
        'email',
        'password'
        )


class UserDemoForm(forms.ModelForm):
    Gender = forms.ChoiceField(choices = GENDER_CHOICES, label="Gender:", widget=forms.Select(), required=True)
    Age = forms.ChoiceField(choices = AGE_CHOICES, required=True)
    Occupation = forms.ChoiceField(choices = JOB_CHOICES, required=True)

    class Meta:
        model = UserProfile
        fields = ('Gender', 'Age', 'Occupation' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save details'))
