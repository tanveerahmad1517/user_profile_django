from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from PIL import Image

from . import forms


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:edit_profile'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    current_user = request.user
    return render(request, 'accounts/profile.html', {'user': current_user})


@login_required
def edit_profile(request):
    user = request.user
    user_form = forms.UserForm(instance=user,
                               initial={'verify_email': user.email})
    formset = forms.UserProfileInlineFormSet(instance=user)

    if request.method == 'POST':
        user_form = forms.UserForm(instance=user,
                                   data=request.POST, files=request.FILES)
        formset = forms.UserProfileInlineFormSet(instance=user,
                                                 data=request.POST,
                                                 files=request.FILES)
        if user_form.is_valid() and formset.is_valid():
            user_form.save()
            for form in formset:
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
            messages.success(request, "User profile updated.")
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/edit_profile.html',
                  {'form': user_form, 'formset': formset, 'user': user})


@login_required
def change_password(request):
    form = forms.ChangePasswordForm(user=request.user)
    if request.method == 'POST':
        form = forms.ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def edit_avatar(request):
    user = request.user
    form = forms.ChangeAvatarForm(instance=user.profile)
    if request.method == 'POST':
        form = forms.ChangeAvatarForm(instance=user.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            avatar = form.save()
            if avatar.avatar:
                # Resize avatar to a particular width and height.
                image = Image.open(avatar.avatar.path)
                image.thumbnail((600, 600))
                image.save(avatar.avatar.path)
            messages.success(request, "User avatar updated.")
            return HttpResponseRedirect(reverse('accounts:edit_avatar'))
    return render(request, 'accounts/edit_avatar.html', {'form': form, 'user': user})


@login_required
def edit_avatar_crop(request):
    user = request.user
    x1 = request.GET['x1']
    y1 = request.GET['y1']
    x2 = request.GET['x2']
    y2 = request.GET['y2']
    if x1 and y1 and x2 and y2 and x1 != x2 and y1 != y2:
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        image = Image.open(user.profile.avatar.path)
        box = (x1, y1, x2, y2)
        image = image.crop(box=box)
        image.save(user.profile.avatar.path)
    return HttpResponseRedirect(reverse('accounts:edit_avatar'))


@login_required
def edit_avatar_rotate(request):
    user = request.user
    image = Image.open(user.profile.avatar.path)
    image = image.transpose(Image.ROTATE_270)
    image.save(user.profile.avatar.path)
    return HttpResponseRedirect(reverse('accounts:edit_avatar'))


@login_required
def edit_avatar_flip(request):
    user = request.user
    image = Image.open(user.profile.avatar.path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(user.profile.avatar.path)
    return HttpResponseRedirect(reverse('accounts:edit_avatar'))