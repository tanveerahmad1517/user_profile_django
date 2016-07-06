import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from uuid import uuid4


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/<filename>, where filename will be
    # given a random value.
    extension = filename.split('.')[-1]

    filename = '{}.{}'.format(uuid4().hex, extension)
    return 'images/{}'.format(filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    bio = models.TextField(blank=False, null=False, default="My biography.")
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

