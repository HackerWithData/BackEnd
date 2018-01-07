import string

from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required
# from django.utils.translation import pgettext, ugettext, ugettext_lazy as _

from allauth.account.forms import SignupForm

from professionals.utils import ENTITY_CHOICES, P, S, C, PROFESSIONAL_CHOICES, PROFESSIONAL_SUBTYPE_CHOICES, CONTRACTOR, \
    ARCHITECT, DESIGNER
from professionals.models import Professional, ProfessionalType
from meisters.models import Meister
from .models import User, ConsumerProfile, ProfessionalProfile
from .user_helpers import get_professional_corresponding_object_by_type_and_lic, \
    create_professional_corresponding_object
from .utils import *

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

    # hoome_id = forms.IntegerField(widget=forms.HiddenInput(),required=False)

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
        label=_('First Name'),
    )

    last_name = forms.CharField(
        required=True,
        max_length=128,
        label=_('Last Name'),
    )

    zipcode = forms.CharField(
        required=True,
        max_length=5,
        min_length=5,
        label=_('Zipcode'),
    )

    gender = forms.MultipleChoiceField(
        required=True,
        choices=GENDER_CHOICES,
        label=_("Gender")
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


class ProfessionalInfoFillUpForm(forms.Form):
    """
        Professional information form after sign up
    """
    license_num = forms.CharField(
        required=True,
        label=_('License Number'),
        widget=forms.TextInput(attrs={'class': 'input-license-number'}),
        initial=0
    )

    professional_type = forms.ChoiceField(
        required=True,
        choices=PROFESSIONAL_CHOICES,
        initial=CONTRACTOR,
        label=_('Professional Type'),
        widget=forms.RadioSelect(attrs={'class': 'input-professional-type'})
    )

    professional_subtype = forms.MultipleChoiceField(
        required=True,
        choices=PROFESSIONAL_SUBTYPE_CHOICES,
        label=_('Field Selections'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'input-professional-subtype'})
    )

    # personal_name = forms.CharField(
    #     required=True,
    #     max_length=255,
    #     label=_('Name'),
    #     widget=forms.TextInput(attrs={'class': 'input-personal-name'})
    # )

    company_name = forms.CharField(
        required=True,
        max_length=255,
        label=_('Name'),
        widget=forms.TextInput(attrs={'class': 'input-company-name'})
    )

    entity_type = forms.ChoiceField(
        required=True,
        choices=ENTITY_CHOICES,
        initial=C,
        label=_('Entity Type'),
        widget=forms.RadioSelect(attrs={'class': 'input-entity-type'})
    )

    street = forms.CharField(
        required=True,
        max_length=128,
        label=_('Street'),
        widget=forms.TextInput(attrs={'class': 'input-street'})
    )

    state = forms.CharField(
        required=True,
        max_length=32,
        label=_('State'),
        widget=forms.TextInput(attrs={'class': 'input-state'})
    )
    county = forms.CharField(
        required=True,
        max_length=32,
        label=_('County'),
        widget=forms.TextInput(attrs={'class': 'input-county'})
    )
    zipcode = forms.CharField(
        required=True,
        max_length=16,
        label=_('Postal Code'),
        widget=forms.TextInput(attrs={'class': 'input-zipcode'})
    )

    # TODO; need to change this part since lic_num is not numberic sometimes
    def clean_license_num(self):
        lic = self.cleaned_data['license_num']
        lic_num = str(lic.strip(string.ascii_letters))
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
        # print subtype
        return subtype

    def save(self, request):
        exists = False
        clean_license_num = self.cleaned_data['license_num']
        # clean_personal_name = self.cleaned_data['personal_name']
        clean_company_name = self.cleaned_data['company_name']
        clean_street = self.cleaned_data['street']
        clean_state = self.cleaned_data['state']
        clean_county = self.cleaned_data['county']
        clean_zipcode = self.cleaned_data['zipcode']
        clean_entity_type = self.cleaned_data['entity_type']
        clean_professional_type = self.cleaned_data['professional_type']
        clean_professional_subtype = self.cleaned_data['professional_subtype']
        # print(clean_professional_type)
        if str(clean_professional_type) == "MEISTER":
            # professional_object = create_professional_corresponding_object(prof_type=clean_professional_type)
            meister, created = Meister.objects.get_or_create(lic_name=clean_company_name,
                                                             # bus_name=clean_company_name,
                                                             street_address=clean_street,
                                                             county=clean_county,
                                                             state=clean_state,
                                                             pos_code=clean_zipcode)
            if created:
                meister.save()
                #TODO: need to change here
                meister.lic_num = meister.lic_id
                meister.save()
            else:
                pass
            # TODO: need to consider if meister is mutually exclusive with other type??
            professional, created = Professional.objects.get_or_create(lic_num=meister.lic_num,
                                                                       name=clean_company_name,
                                                                       entity_type=clean_entity_type,
                                                                       lic_type='&'.join(clean_professional_subtype),
                                                                       type=clean_professional_type,
                                                                       county=clean_county,
                                                                       state=clean_state,
                                                                       postal_code=clean_zipcode)
            if created:
                professional.save()
            else:
                pass

        else:
            # TODO: need to fix later
            if "tx" in clean_state.lower() or "texas" in clean_state.lower():
                clean_license_num = "TX" + str(clean_license_num)
            professional_qs = Professional.objects.filter(lic_num=clean_license_num, type=clean_professional_type)
            # print professional_qs
            # find the result
            if professional_qs.exists() and professional_qs.count() == 1:
                exists = True
                professional = professional_qs.first()
                professional.entity_type = clean_entity_type
                professional.county = clean_county
                professional.state = clean_state
                professional.postal_code = clean_zipcode
                # save professional
                professional.save()
                professional_object = get_professional_corresponding_object_by_type_and_lic(
                    prof_type=clean_professional_type,
                    lic=clean_license_num)
                professional_object.bus_name = clean_company_name
                professional_object.entity = clean_entity_type
                professional_object.state = clean_state
                professional_object.county = clean_county
                professional_object.street_address = clean_street
                professional_object.pos_code = clean_zipcode
                professional_object.save()
            # multiple item for the same professional
            elif professional_qs.count() > 1:
                raise MultipleSameProfessionalFound('Found Redundant Professionals')
            # create new professional
            else:
                professional = Professional.objects.create(lic_num=clean_license_num,
                                                           name=clean_company_name,
                                                           entity_type=clean_entity_type,
                                                           type=clean_professional_type,
                                                           lic_type='&'.join(clean_professional_subtype),
                                                           state=clean_state,
                                                           postal_code=clean_zipcode)
                professional.save()
                professional_object = create_professional_corresponding_object(prof_type=clean_professional_type,
                                                                               lic=clean_license_num)
                professional_object.lic_name = clean_company_name
                professional_object.entity = clean_entity_type
                professional_object.state = clean_state
                professional_object.county = clean_county
                professional_object.csp = clean_county + ' ' + clean_state + ', ' + clean_zipcode
                professional_object.street_address = clean_street
                professional_object.pos_code = clean_zipcode
                professional_object.save()

        user = request.user
        # TODO: Need to change code here. there is a bug here.
        # create new profile
        try:
            ProfessionalProfile.objects.create(user=user, professional=professional)
        except:
            pass
        professionaltypes = ProfessionalType.objects.filter(professional_id=professional.pk)
        # create new subtypes for profile
        existing_prof_types = [pt.subtype for pt in professionaltypes]
        for subtype in clean_professional_subtype:
            if subtype not in existing_prof_types:
                ProfessionalType.objects.create(professional=professional,
                                                type=clean_professional_type,
                                                subtype=subtype)


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
        profile = user.consumer_profiles.first()
        profile.gender = clean_gender
        profile.zipcode = clean_zipcode
        profile.save()


class ProfessionalProfileEditForm(ProfessionalInfoFillUpForm):
    """
        Professional information form after sign up
    """

    license_num = forms.CharField(
        required=True,
        label=_('License Number'),
        widget=forms.TextInput(attrs={'class': 'input-license-number', 'readonly': 'true'})
    )

    # company_name = forms.CharField(
    #     required=True,
    #     max_length=128,
    #     label=_('Name'),
    #     widget=forms.TextInput(attrs={'class': 'input-company-name', 'readonly': 'true'})
    # )

    professional_type = forms.ChoiceField(
        required=True,
        choices=PROFESSIONAL_CHOICES,
        initial=CONTRACTOR,
        label=_('Professional Type'),
        widget=forms.RadioSelect(attrs={'class': 'input-professional-type', 'readonly': 'true'})
    )

    def save(self, request):
        # Cannot be changed
        clean_license_num = self.cleaned_data['license_num']
        # clean_company_name = self.cleaned_data['company_name']
        clean_street = self.cleaned_data['street']
        clean_state = self.cleaned_data['state']
        clean_zipcode = self.cleaned_data['zipcode']
        clean_entity_type = self.cleaned_data['entity_type']
        clean_county = self.cleaned_data['county']
        clean_professional_type = self.cleaned_data['professional_type']

        clean_professional_subtype = self.cleaned_data['professional_subtype']

        profile = request.user.professional_profiles.first()
        professional = profile.professional

        professionaltypes = ProfessionalType.objects.filter(professional_id=professional.pk)
        # create new subtypes for profile
        existing_prof_types = [pt.subtype for pt in professionaltypes]
        current_prof_types = list(existing_prof_types)
        for subtype in clean_professional_subtype:
            if subtype not in existing_prof_types:
                ProfessionalType.objects.create(professional=professional,
                                                type=clean_professional_type,
                                                subtype=subtype)
                current_prof_types.append(subtype)

        professional.state = clean_state
        professional.county = clean_county
        professional.postal_code = clean_zipcode
        professional.entity_type = clean_entity_type
        professional.lic_type = '&'.join(current_prof_types)
        professional.save()
        professional_object = get_professional_corresponding_object_by_type_and_lic(prof_type=clean_professional_type,
                                                                                    lic=clean_license_num)
        professional_object.street_address = clean_street
        professional_object.save()


class MultipleSameProfessionalFound(Exception):
    pass
