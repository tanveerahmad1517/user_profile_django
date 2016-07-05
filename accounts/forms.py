import bleach

from bs4 import BeautifulSoup
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core import validators
from html5.forms import widgets as html5_widgets


from . import models


forms.DateField.default_error_messages = {
    'invalid': "Date should be of the following format: YYYY-MM-DD, MM/DD/YY,"
               " or MM/DD/YYYY."
}


def longer_than_9(value):
    if len(value) < 10:
        raise forms.ValidationError('must be 10 characters or longer')


class UserForm(forms.ModelForm):
    verify_email = forms.EmailField(
        label="Please verify your email address",
        required=True,
        validators=[validators.EmailValidator()]
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'verify_email',
        ]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if 'email' not in cleaned_data or 'verify_email' not in cleaned_data:
            return cleaned_data
        email = cleaned_data['email']
        verify_email = cleaned_data['verify_email']
        if email != verify_email:
            raise forms.ValidationError(
                "You need to enter the same email in both fields.")


class ProfileForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        fields = [
#            'avatar',
            'date_of_birth',
            'bio'
        ]
        widgets = {
            'date_of_birth': html5_widgets.DateInput,
        }

    def clean_bio(self):
        soup = BeautifulSoup(self.cleaned_data['bio'], "html.parser")
        if len(soup.get_text().strip()) < 10:
            raise forms.ValidationError('Bio must be 10 characters or longer')
        return self.cleaned_data['bio']


class ChangePasswordForm(PasswordChangeForm):
    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        if 'new_password1' not in cleaned_data or (
                    'old_password' not in cleaned_data):
            return cleaned_data
        new_password1 = cleaned_data['new_password1']
        old_password = cleaned_data['old_password']
        if new_password1 == old_password:
            raise forms.ValidationError(
                "New password must be different from the current one."
            )


class ChangeAvatarForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        fields = ['avatar']

UserProfileInlineFormSet = forms.inlineformset_factory(
    User,
    models.Profile,
    ProfileForm,
    fields=(
#        'avatar',
        'date_of_birth', 'bio'),
    can_delete=False
)