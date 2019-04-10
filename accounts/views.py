from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
    UserDemoForm
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *

#Registering user

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(
            username = username,
            password = password
            )
            login(request, user)
            return redirect('/account/adding_details/')
    else:
        form = RegistrationForm()

    args = {'form':form}
    return render(request, 'accounts/reg_form.html',args)


def view_profile(request, pk=None):
    storage = messages.get_messages(request)
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user, 'message':storage}
    return render(request, 'accounts/profile.html', args)

def Add_demo_details(request):
    template_name =  'accounts/adding_details.html'
    instance = UserProfile.objects.get(user_id=request.user.id)
    form = UserDemoForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/account/profile')
    args = {'form':form}
    return render(request, template_name, args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance= request.user )

        if form.is_valid():
            form.save()
            return redirect('/account/profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'accounts/edit_profile.html', args)

#login is required to change password

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Pasword changed successfully')
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')

    else:
        form = PasswordChangeForm(user=request.user)

    args = {'form':form}
    return render(request, 'accounts/change_password.html',args)
