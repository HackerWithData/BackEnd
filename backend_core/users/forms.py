from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _

from models import User, ConsumerProfile, ProfessionalProfile
from professionals.utils import ENTITY_CHOICES, P, S, C, PROFESSIONAL_CHOICES, PROFESSIONAL_SUBTYPE_CHOICES, CONTRACTOR, ARCHITECT, DESIGNER
from professionals.models import Professional, ProfessionalType
from user_helpers import get_professional_corresponding_object, create_professional_corresponding_object
from utils import *
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __

import string

professional_type = setup_professional_type()


class UserSignUpForm(SignupForm):
    """
        User sign up form
    """
    # TODO: change role type in form, part 1
    role = forms.MultipleChoiceField(
        required=True,
        choices=ROLE_CHOICES
    )

    def clean_role(self):
        # TODO: change role type in form, part 2
        role = self.cleaned_data['role']
        if role[0] not in [choice[0] for choice in ROLE_CHOICES]:
            raise forms.ValidationError(_('Must select a role'))
        return role[0]


class ConsumerInfoFillUpForm(forms.Form):
    """
        Consumer information form after sign up
    """
    first_name = forms.CharField(
        required=True,
        max_length=128,
        label=__('First Name'),
    )

    last_name = forms.CharField(
        required=True,
        max_length=128,
        label=__('Last Name'),
    )

    zipcode = forms.CharField(
        required=True,
        max_length=5,
        min_length=5,
        label=__('Zipcode'),
    )

    gender = forms.MultipleChoiceField(
        required=True,
        choices=GENDER_CHOICES,
        label=__("Gender")
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
    """
        Professional information form after sign up
    """
    license_num = forms.CharField(
        required=True,
        label=__('License Number'),
        widget=forms.TextInput(attrs={'class': 'input-license-number'})
    )

    professional_type = forms.ChoiceField(
        required=True,
        choices=PROFESSIONAL_CHOICES,
        initial=CONTRACTOR,
        label=__('Professional Type'),
        widget=forms.RadioSelect(attrs={'class': 'input-professional-type'})
    )

    professional_subtype = forms.MultipleChoiceField(
        required=True,
        choices=PROFESSIONAL_SUBTYPE_CHOICES,
        label=__('Field Selections'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'input-professional-subtype'})
    )

    company_name = forms.CharField(
        required=True,
        max_length=128,
        label=__('Name'),
        widget=forms.TextInput(attrs={'class': 'input-company-name'})
    )

    entity_type = forms.ChoiceField(
        required=True,
        choices=ENTITY_CHOICES,
        initial=C,
        label=__('Entity Type'),
        widget=forms.RadioSelect(attrs={'class': 'input-entity-type'})
    )

    street = forms.CharField(
        required=True,
        max_length=128,
        label=__('Street'),
        widget=forms.TextInput(attrs={'class': 'input-street'})
    )

    state = forms.CharField(
        required=True,
        max_length=32,
        label=__('State'),
        widget=forms.TextInput(attrs={'class': 'input-state'})
    )

    zipcode = forms.CharField(
        required=True,
        max_length=16,
        label=__('Postal Code'),
        widget=forms.TextInput(attrs={'class': 'input-zipcode'})
    )

    def clean_license_num(self):
        lic = self.cleaned_data['license_num']
        lic_num = int(lic.strip(string.ascii_letters))
        return lic_num

    def clean_professional_type(self):
        professional = self.cleaned_data['professional_type']
        if professional not in [choice[0] for choice in PROFESSIONAL_CHOICES]:
            raise forms.ValidationError(_('Must select a professional type'))
        return professional

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
        print subtype
        return subtype

    def save(self, request):
        exists = False
        clean_license_num = self.cleaned_data['license_num']
        clean_company_name = self.cleaned_data['company_name']
        clean_street = self.cleaned_data['street']
        clean_state = self.cleaned_data['state']
        clean_zipcode = self.cleaned_data['zipcode']
        clean_entity_type = self.cleaned_data['entity_type']
        clean_professional_type = self.cleaned_data['professional_type']
        clean_professional_subtype = self.cleaned_data['professional_subtype']

        professional_qs = Professional.objects.filter(lic_num=clean_license_num, type=clean_professional_type)
        print professional_qs
        # find the result
        if professional_qs.exists() and professional_qs.count() == 1:
            exists = True
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
        # TODO: Need to change code here. there is a bug here.
        # create new profile
        ProfessionalProfile.objects.create(user=user, professional=professional)
        professionaltypes = ProfessionalType.objects.filter(professional_id=professional.pk)
        # create new subtypes for profile
        existing_prof_types = [pt.subtype for pt in professionaltypes]
        for subtype in clean_professional_subtype:
            if subtype not in existing_prof_types:
                ProfessionalType.objects.create(professional=professional,
                                                type=clean_professional_type,
                                                subtype=subtype)

        if exists:
            # get existing corresponding professional
            professional_object = get_professional_corresponding_object(prof_type=clean_professional_type,
                                                                        lic=clean_license_num)
        else:
            # create new corresponding professional
            professional_object = create_professional_corresponding_object(prof_type=clean_professional_type,
                                                                           lic=clean_license_num)
        professional_object.bus_name = clean_company_name
        professional_object.entity = clean_entity_type
        professional_object.state = clean_state
        professional_object.street_address = clean_street
        professional_object.pos_code = clean_zipcode
        professional_object.save()


class ConsumerProfileEditForm(ConsumerInfoFillUpForm):
    """
        Consumer information form edit in dashboard
    """
    def save(self, request):
        clean_gender = self.cleaned_data['gender']
        clean_first_name = self.cleaned_data['first_name']
        clean_last_name = self.cleaned_data['last_name']
        clean_zipcode = self.cleaned_data['zipcode']
        user = request.user
        user.first_name = clean_first_name
        user.last_name = clean_last_name
        user.save()
        profile = ConsumerProfile.consumer_profiles.first()
        profile.gender = clean_gender
        profile.zipcode = clean_zipcode
        profile.save()


class ProfessionalProfileEditForm(ProfessionalInfoFillUpForm):
    """
        Professional information form after sign up
    """

    license_num = forms.CharField(
        required=True,
        label=__('License Number'),
        widget=forms.TextInput(attrs={'class': 'input-license-number', 'readonly': 'true'})
    )

    company_name = forms.CharField(
        required=True,
        max_length=128,
        label=__('Name'),
        widget=forms.TextInput(attrs={'class': 'input-company-name', 'readonly': 'true'})
    )

    professional_type = forms.ChoiceField(
        required=True,
        choices=PROFESSIONAL_CHOICES,
        initial=CONTRACTOR,
        label=__('Professional Type'),
        widget=forms.RadioSelect(attrs={'class': 'input-professional-type', 'readonly': 'true'})
    )

    def save(self, request):
        # Cannot be changed
        clean_license_num = self.cleaned_data['license_num']
        clean_company_name = self.cleaned_data['company_name']
        clean_street = self.cleaned_data['street']
        clean_state = self.cleaned_data['state']
        clean_zipcode = self.cleaned_data['zipcode']
        clean_entity_type = self.cleaned_data['entity_type']
        # Cannot be changed
        clean_professional_type = self.cleaned_data['professional_type']

        clean_professional_subtype = self.cleaned_data['professional_subtype']
        profile = request.user.professional_profiles.first()
        professional = profile.professional
        professional.state = clean_state
        professional.postal_code = clean_zipcode
        professional.entity_type = clean_entity_type
        professional.save()

        professional_object = get_professional_corresponding_object(prof_type=clean_professional_type, lic=clean_license_num)
        professional_object.street_address = clean_street
        professional_object.save()

        professionaltypes = ProfessionalType.objects.filter(professional_id=professional.pk)
        # create new subtypes for profile
        existing_prof_types = [pt.subtype for pt in professionaltypes]
        for subtype in clean_professional_subtype:
            if subtype not in existing_prof_types:
                ProfessionalType.objects.create(professional=professional,
                                                type=clean_professional_type,
                                                subtype=subtype)


class MultipleSameProfessionalFound(Exception):
    pass


