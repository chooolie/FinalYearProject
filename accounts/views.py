from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse


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
            return redirect('/home')
    else:
        form = RegistrationForm()

    args = {'form':form}
    return render(request, 'accounts/reg_form.html',args)

#Login is required to view profile


def view_profile(request, pk=None):
    storage = messages.get_messages(request)
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user, 'message':storage}
    return render(request, 'accounts/profile.html', args)

#Log in is rquired to edit profile

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance= request.user)

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
