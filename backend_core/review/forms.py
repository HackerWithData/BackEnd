import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as __
from django.contrib.contenttypes.models import ContentType

from projects.utils import (PROJECT_TYPE, MILESTONE_STATUS, REMODEL, WAITING)
from .models import Review


def name_validator(name):
    if not name.isalpha():
        raise ValidationError(__('name must contain only alphabetic characters'), code='name_error')


def zipcode_validator(zipcode):
    rex = re.compile(r'^\d{5}(?:[-\s]\d{4})?$')
    if not rex.match(zipcode):
        raise ValidationError(__('zipcode format should be xxxxx or xxxxx-xxxx'), code='zipcode_error')


# def positive_int_validator(num):
#     if num < 0:
#         raise ValidationError(_('cannot be a negative number'), code='cost_error')


def email_validator(email):
    rex = re.compile(r'^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$')
    if not rex.match(email):
        raise ValidationError(__('invalid email address'), code='email_error')


class ReviewForm(forms.Form):
    comments = forms.CharField(label=__('Comments*'), widget=forms.Textarea)
    first_name = forms.CharField(label=__('First Name*'), max_length=25, validators=[name_validator])
    last_name = forms.CharField(label=__('Last Name*'), max_length=25, validators=[name_validator])
    project_date = forms.DateField(label=__('When did the project start?*'), widget=forms.SelectDateWidget())
    project_type = forms.ChoiceField(choices=PROJECT_TYPE, label=__('Project Type*'))
    project_cost = forms.IntegerField(label=__('Project Cost*'), min_value=0)
    project_duration = forms.IntegerField(label=__('How many days does the project take?*'), min_value=0)
    email = forms.CharField(label=__('Email*'), max_length=254, validators=[email_validator])
    street_address = forms.CharField(label=__('Street Address*'))
    street_address2 = forms.CharField(label=__('Apt #, Suite #, ...'), required=False,
                                      widget=forms.TextInput(attrs={'placeholder': __("(Optional) Apt #,Suite #,...")}))
    county = forms.CharField(label=__('County/City*'), max_length=64)
    state = forms.CharField(label=__('State*'), max_length=64)
    zipcode = forms.CharField(label=__('Zip Code*'), max_length=10,validators=[zipcode_validator])
    is_anonymous = forms.BooleanField(label=__('Is Anonymous?'), required=False)

    def save(self, commit=True):
        review = Review(comments=self.cleaned_data['comments'],
                        first_name=self.cleaned_data['first_name'],
                        last_name=self.cleaned_data['last_name'],
                        project_date=self.cleaned_data['project_date'],
                        project_type=self.cleaned_data['project_type'],
                        project_cost=self.cleaned_data['project_cost'],
                        project_duration=self.cleaned_data['project_duration'],
                        email=self.cleaned_data['email'],
                        street_address=self.cleaned_data['street_address'],
                        street_address2=self.cleaned_data['street_address2'],
                        county=self.cleaned_data['county'],
                        state=self.cleaned_data['state'],
                        zipcode=self.cleaned_data['zipcode'],
                        is_anonymous=self.cleaned_data['is_anonymous'])
        if commit:
            review.save()
        return review
