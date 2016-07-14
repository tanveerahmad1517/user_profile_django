from django import template


register = template.Library()


@register.filter('underscore_to_space')
def underscore_to_space(string):
    """Changes underscore to a space."""
    new_string = string.replace('_', ' ')
    return new_string
