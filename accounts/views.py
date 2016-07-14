from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from PIL import Image

from . import forms


def sign_in(request):
    """Sign in view."""
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('accounts:profile'))
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
    """Sign up view."""
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
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    """Sign out view."""
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    """User profile view."""
    user = request.user
    user_data = [
        ('first_name', user.first_name),
        ('last_name', user.last_name),
        ('email', user.email),
        ('date_of_birth', user.profile.date_of_birth),
        ('website', user.profile.website),
        ('country', user.profile.country),
        ('bio', user.profile.bio),
    ]

    # Remove items with NULL values
    cleaned_user_data = [(key, value) for key, value in user_data if value]

    return render(request, 'accounts/profile.html', {
        'user_data': cleaned_user_data})


@login_required
def edit_profile(request):
    """View to edit user profile."""
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
                user_profile = form.save(commit=False)
                user_profile.user = user
                user_profile.save()
            messages.success(request, "User profile updated.")
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/edit_profile.html',
                  {'form': user_form, 'formset': formset})


@login_required
def change_password(request):
    """View to change password."""
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
    """View to edit avatar."""
    user = request.user
    form = forms.ChangeAvatarForm(instance=user.profile)
    if request.method == 'POST':
        form = forms.ChangeAvatarForm(
            instance=user.profile,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            avatar = form.save()

            if avatar.avatar:
                # Resize avatar to a particular width and height.
                image = Image.open(avatar.avatar.path)
                image.thumbnail((600, 600))
                image.save(avatar.avatar.path)
            messages.success(request, "User avatar updated.")
            return HttpResponseRedirect(reverse('accounts:edit_avatar'))
    return render(request, 'accounts/edit_avatar.html', {'form': form})


@login_required
def edit_avatar_crop(request):
    """Crops user avatar."""
    user = request.user
    left = request.GET['x1']
    top = request.GET['y1']
    right = request.GET['x2']
    bottom = request.GET['y2']
    if left and top and right and bottom and left != right and top != bottom:
        left = int(left)
        top = int(top)
        right = int(right)
        bottom = int(bottom)
        image = Image.open(user.profile.avatar.path)
        box = (left, top, right, bottom)
        image = image.crop(box=box)
        image.save(user.profile.avatar.path)
    return HttpResponseRedirect(reverse('accounts:edit_avatar'))


@login_required
def edit_avatar_rotate(request):
    """Rotates user avatar."""
    user = request.user
    image = Image.open(user.profile.avatar.path)
    image = image.transpose(Image.ROTATE_270)
    image.save(user.profile.avatar.path)
    return HttpResponseRedirect(reverse('accounts:edit_avatar'))


@login_required
def edit_avatar_flip(request):
    """Flips user avatar."""
    user = request.user
    image = Image.open(user.profile.avatar.path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(user.profile.avatar.path)
    return HttpResponseRedirect(reverse('accounts:edit_avatar'))
