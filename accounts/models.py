from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.db import models


class Profile(models.Model):
    """User profile model class."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    country = CountryField(blank=True, null=True, blank_label='Select country')


def create_profile(sender, **kwargs):
    """Create Profile instance whenever User is created."""
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)
