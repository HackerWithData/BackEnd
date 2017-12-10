import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_lazy as __


def name_validator(name):
    if not name.isalpha():
        raise ValidationError(_('name must contain only alphabetic characters'), code='name_error')


def zipcode_validator(zipcode):
    rex = re.compile(r'^\d{5}(?:[-\s]\d{4})?$')
    if not rex.match(zipcode):
        raise ValidationError(_('zipcode format should be xxxxx or xxxxx-xxxx'), code='zipcode_error')


# def positive_int_validator(num):
#     if num < 0:
#         raise ValidationError(_('cannot be a negative number'), code='cost_error')


def email_validator(email):
    rex = re.compile(r'^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$')
    if not rex.match(email):
        raise ValidationError(_('invalid email address'), code='email_error')


class ReviewForm(forms.Form):
    comments = forms.CharField(label=_('Comments*'), widget=forms.Textarea)
    first_name = forms.CharField(label=_('First Name*'), max_length=25, validators=[name_validator])
    last_name = forms.CharField(label=_('Last Name*'), max_length=25, validators=[name_validator])
    project_date = forms.DateField(label=_('Project Date*'), widget=forms.SelectDateWidget())
    project_type = forms.CharField(label=_('Project Type*'), max_length=255)
    project_zipcode = forms.CharField(label=_('Project Zipcode*'), max_length=20, validators=[zipcode_validator])
    project_cost = forms.IntegerField(label=_('Project Cost*'), min_value=0)
    project_duration = forms.IntegerField(label=_('How many days does the project take?*'), min_value=0)
    email = forms.CharField(label=_('Email*'), max_length=254, validators=[email_validator])
    street_address = forms.CharField(label=__('Street Address*'))
    street_address2 = forms.CharField(label=__('Apt #, Suite #, ...'), required=False,
                                      widget=forms.TextInput(attrs={'placeholder': __("(Optional) Apt #,Suite #,...")}))
    county = forms.CharField(label=__('County/City*'), max_length=64)
    state = forms.CharField(label=__('State*'), max_length=64)
    zipcode = forms.CharField(label=__('Zip Code*'), max_length=10)
    is_anonymous = forms.BooleanField(label=_('Is Anonymous?'), required=False)
