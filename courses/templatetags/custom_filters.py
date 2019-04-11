import random
import datetime

from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings
# from cabalahi_sites.models import CabalahiSite


register    =   template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__

@register.filter
def input_class(bound_field):
    css_class   =   ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class   =   'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class   =   'is-valid'
    return 'form-control {}'.format(css_class)

@register.filter
def add_validation_class_sm(bound_field):
    validation_class = 'form-control'
    if bound_field.form.is_bound:
        if bound_field.errors:
            validation_class += ' is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            validation_class += ' is-valid'
    return bound_field.as_widget(attrs={'class': validation_class})

@register.filter
def add_validation_class(bound_field):
    validation_class = 'form-control form-control-lg'
    if bound_field.form.is_bound:
        if bound_field.errors:
            validation_class += ' is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            validation_class += ' is-valid'
    return bound_field.as_widget(attrs={'class': validation_class})

@register.filter
def icon_picker_add_validation_class(bound_field):
    validation_class = 'icon-picker-input form-control form-control-lg'
    if bound_field.form.is_bound:
        if bound_field.errors:
            validation_class += ' is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            validation_class += ' is-valid'
    return bound_field.as_widget(attrs={'class': validation_class})

@register.filter(name='phone_number')
@stringfilter
def phone_number(number):
    """Convert a 8 character string into (xxx) xxxx xxxx."""
    first = number[0:4]
    second = number[4:8]
    third = number[8:12]
    return first + ' ' + second + ' ' + third

@register.simple_tag
def random_color():
    colors = ['#9F86FF', '#1BC98E','#E64759', '#007bff']
    random_color = str(random.choice(colors))
    return random_color