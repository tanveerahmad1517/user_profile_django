from bs4 import BeautifulSoup
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core import validators
from django_countries.widgets import CountrySelectWidget
from html5.forms import widgets as html5_widgets


from . import models


forms.DateField.default_error_messages = {
    'invalid': "Date should be of the following format: YYYY-MM-DD, MM/DD/YY,"
               " or MM/DD/YYYY."
}


def longer_than_9(value):
    """Checks that the length of input data is 10 characters or longer."""
    if len(value) < 10:
        raise forms.ValidationError('must be 10 characters or longer')


class UserForm(forms.ModelForm):
    """Form for standard user information."""
    verify_email = forms.EmailField(
        label="Please verify your email address",
        required=False,
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

    def clean(self):
        """Check that emails match."""
        cleaned_data = super(UserForm, self).clean()
        if 'email' not in cleaned_data and 'verify_email' not in cleaned_data:
            return cleaned_data
        elif 'email' in cleaned_data and 'verify_email' in cleaned_data:
            email = cleaned_data['email']
            verify_email = cleaned_data['verify_email']
            print(email, verify_email)
            if email != verify_email:
                raise forms.ValidationError(
                    "You need to enter the same email in both fields.")
        else:
            raise forms.ValidationError(
                "You need to enter the same email in both fields.")


class ProfileForm(forms.ModelForm):
    """Form for additional user information."""
    class Meta:
        model = models.Profile
        fields = [
            'date_of_birth',
            'bio',
            'website',
            'country',
        ]
        widgets = {
            'date_of_birth': html5_widgets.DateInput,
            'country': CountrySelectWidget(
                layout='{widget}'
            ),
        }

    def clean_bio(self):
        """Checks that if bio is present its length is 10 characters or more,
        not taking into consideration HTML formatting."""
        bio = BeautifulSoup(self.cleaned_data['bio'], "html.parser")
        char_num = len(bio.get_text().replace(' ', ''))
        print(char_num)
        if 0 < char_num < 10:
            raise forms.ValidationError('If you want to share bio, make it '
                                        '10 characters or longer')
        return self.cleaned_data['bio']


class ChangePasswordForm(PasswordChangeForm):
    """Form to change user password."""
    def clean(self):
        """Checks that new password is different from the old one."""
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
    """Form to change user avatar."""
    class Meta:
        model = models.Profile
        fields = ['avatar']

UserProfileInlineFormSet = forms.inlineformset_factory(
    User,
    models.Profile,
    ProfileForm,
    fields=('date_of_birth', 'website', 'country', 'bio'),
    can_delete=False
)
