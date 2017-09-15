from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _

import string

from models import User, ConsumerProfile, ProfessionalProfile
from utils import *


class UserSignUpForm(SignupForm):

    # TODO: change role type in form, part 1
    role = forms.MultipleChoiceField(
        required=True,
        choices=ROLE_CHOICES
    )

    def clean_role(self):
        # TODO: change role type in form, part 2
        role = self.cleaned_data['role']
        print role[0]
        print [m for m in self.cleaned_data]
        #print ROLE_CHOICES
        #print [choice[0] for choice in ROLE_CHOICES]
        if role[0] not in [choice[0] for choice in ROLE_CHOICES]:
            raise forms.ValidationError(_('Must select a role'))
        return role[0]


class ConsumerInfoFillUpForm(forms.Form):

    first_name = forms.CharField(
        required=True,
        max_length=128
    )

    last_name = forms.CharField(
        required=True,
        max_length=128
    )

    zipcode = forms.CharField(
        required=True,
        max_length=5,
        min_length=5
    )

    gender = forms.MultipleChoiceField(
        required=True,
        choices=GENDER_CHOICES
    )

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        zip_num = int(zipcode.strip(string.ascii_letters))
        zip_str = str(zip_num)
        if len(zip_str) != 5:
            raise forms.ValidationError(_('Invalid zipcode'))
        return zip_str

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender not in [choice[0] for choice in GENDER_CHOICES]:
            raise forms.ValidationError(_('Must select a gender'))
        return gender

    def clean(self):
        cleaned_data = super(UserSignUpForm, self).clean()
        return cleaned_data

    def save(self, request):
        gender = self.cleaned_data['gender']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        zipcode = self.cleaned_data['zipcode']
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile = ConsumerProfile(user=user, gender=gender, zipcode=zipcode)
        profile.save()



"""
class UserChangeForm(forms.ModelForm):
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User#get_user_model()
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
"""