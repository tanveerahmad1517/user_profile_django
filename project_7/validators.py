import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class UpperLowerCaseValidator(object):
    """Checks that password contains both upper and lower case letters."""
    def validate(self, password, user=None):
        if not re.search(r'[a-z]+', password) or (
                not re.search(r'[A-Z]+', password)):
            raise ValidationError(
                _("Your password doesn't contain both uppercase and lowercase"
                  " letters."),
            )

    def get_help_text(self):
        return _(
            "Your password must contain both uppercase and lowercase letters."
        )


class ContainsNumberValidator(object):
    """Checks that password contains at least one number."""
    def validate(self, password, user=None):
        if not re.search(r'[0-9]+', password):
            raise ValidationError(
                _("Your password doesn't contain numerical digits."),
            )

    def get_help_text(self):
        return _(
            "Your password must contain one or more numerical digits."
        )


class ContainsSpecialCharactersValidator(object):
    """Checks that password contains at least one special character."""
    def validate(self, password, user=None):
        if not re.search(r'[0-9]+', password):
            raise ValidationError(
                _("Your password doesn't contain special characters, such as"
                  " @, #, $."),
            )

    def get_help_text(self):
        return _(
            "Your password must contain special characters, such as @, #, $."
        )
