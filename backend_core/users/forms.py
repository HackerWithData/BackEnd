from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _

from models import User, ConsumerProfile, ProfessionalProfile
from professionals.utils import ENTITY_CHOICES, P, S, C, PROFESSIONAL_CHOICES, PROFESSIONAL_SUBTYPE_CHOICES, CONTRACTOR, ARCHITECT, DESIGNER
from professionals.models import Professional, ProfessionalType
from utils import *

import string

professional_type = setup_professional_type()


class UserSignUpForm(SignupForm):

    # TODO: change role type in form, part 1
    role = forms.MultipleChoiceField(
        required=True,
        choices=ROLE_CHOICES
    )

    def clean_role(self):
        # TODO: change role type in form, part 2
        role = self.cleaned_data['role']
        # print role[0]
        # print [m for m in self.cleaned_data]
        #print ROLE_CHOICES
        #print [choice[0] for choice in ROLE_CHOICES]
        if role[0] not in [choice[0] for choice in ROLE_CHOICES]:
            raise forms.ValidationError(_('Must select a role'))
        return role[0]


class ConsumerInfoFillUpForm(forms.Form):

    first_name = forms.CharField(
        required=True,
        max_length=128,
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
        if gender[0] not in [choice[0] for choice in GENDER_CHOICES]:
            raise forms.ValidationError(_('Must select a gender'))
        return gender[0]

    def save(self, request):
        clean_gender = self.cleaned_data['gender']
        clean_first_name = self.cleaned_data['first_name']
        clean_last_name = self.cleaned_data['last_name']
        clean_zipcode = self.cleaned_data['zipcode']
        user = request.user
        user.first_name = clean_first_name
        user.last_name = clean_last_name
        user.save()
        profile = ConsumerProfile(user=user, gender=clean_gender, zipcode=clean_zipcode)
        profile.save()


# TODO: implement professional form
class ProfessionalInfoFillUpForm(forms.Form):

    license_num = forms.CharField(
        required=True,
        label='License Number',
        widget=forms.TextInput(attrs={'class': 'input-license-number'})
    )

    professional_type = forms.ChoiceField(
        required=True,
        choices=PROFESSIONAL_CHOICES,
        initial=CONTRACTOR,
        label='Professional Type',
        widget=forms.RadioSelect(attrs={'class': 'input-professional-type'})
    )

    professional_subtype = forms.MultipleChoiceField(
        required=True,
        choices=PROFESSIONAL_SUBTYPE_CHOICES,
        label='Field Selections',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'input-professional-subtype'})
    )

    company_name = forms.CharField(
        required=True,
        max_length=128,
        label='Name',
        widget=forms.TextInput(attrs={'class': 'input-company-name'})
    )

    entity_type = forms.ChoiceField(
        required=True,
        choices=ENTITY_CHOICES,
        initial=C,
        label='Entity Type',
        widget=forms.RadioSelect(attrs={'class': 'input-entity-type'})
    )

    street = forms.CharField(
        required=True,
        max_length=128,
        label='Street',
        widget=forms.TextInput(attrs={'class': 'input-street'})
    )

    state = forms.CharField(
        required=True,
        max_length=32,
        label='State',
        widget=forms.TextInput(attrs={'class': 'input-state'})
    )

    zipcode = forms.CharField(
        required=True,
        max_length=16,
        label='Postal Code',
        widget=forms.TextInput(attrs={'class': 'input-zipcode'})
    )

    def clean_license_num(self):
        lic = self.cleaned_data['license_num']
        lic_num = int(lic.strip(string.ascii_letters))
        return lic_num

    def clean_professional_type(self):
        professional = self.cleaned_data['professional_type']
        if professional[0] not in [choice[0] for choice in PROFESSIONAL_CHOICES]:
            raise forms.ValidationError(_('Must select a professional type'))
        return professional[0]

    def clean_entity_type(self):
        entity = self.cleaned_data['entity_type']
        if entity not in [choice[0] for choice in ENTITY_CHOICES]:
            raise forms.ValidationError(_('Must select a entity type'))
        return entity

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        zip_num = int(zipcode.strip(string.ascii_letters))
        zip_str = str(zip_num)
        if len(zip_str) != 5:
            raise forms.ValidationError(_('Invalid zipcode'))
        return zip_str

    # TODO: validate
    def clean_professional_subtype(self):
        subtype = self.cleaned_data['professional_subtype']
        return subtype

    def save(self, request):
        clean_license_num = self.cleaned_data['license_num']
        clean_company_name = self.cleaned_data['company_name']
        clean_street = self.cleaned_data['street']
        clean_state = self.cleaned_data['state']
        clean_zipcode = self.cleaned_data['zipcode']
        clean_entity_type = self.cleaned_data['entity_type']
        clean_professional_type = self.cleaned_data['professional_type']
        clean_professional_subtype = self.cleaned_data['professional_subtype']

        professional_qs = Professional.objects.filter(lic_num=clean_license_num, type=clean_professional_type)
        # find the result
        if professional_qs.exists() and professional_qs.count() == 1:
            professional = professional_qs.first()
            professional.entity_type = clean_entity_type
            professional.state = clean_state
            professional.postal_code = clean_zipcode
            # save professional
            professional.save()
        # multiple item for the same professional
        elif professional_qs.count() > 1:
            raise MultipleSameProfessionalFound('Found Redundant Professionals')
        # create new professional
        else:
            professional = Professional.objects.create(lic_num=clean_license_num,
                                                       name=clean_company_name,
                                                       entity_type=clean_entity_type,
                                                       type=clean_professional_type,
                                                       state=clean_state,
                                                       postal_code=clean_zipcode)

        user = request.user

        # create new profile
        ProfessionalProfile.objects.create(user=user, professional=professional)

        # create new subtypes for profile
        for subtype in clean_professional_subtype:
            ProfessionalType.objects.create(professional=professional,
                                            type=clean_professional_type,
                                            subtype=subtype)


class MultipleSameProfessionalFound(Exception):
    pass


