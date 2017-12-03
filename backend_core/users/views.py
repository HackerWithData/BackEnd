# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.urlresolvers import reverse_lazy, reverse
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login
from allauth.account.views import PasswordChangeView, PasswordSetView
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from allauth.account.views import LoginView
from django.contrib import messages
from professionals.models import Professional, ProfessionalType
from forms import ConsumerInfoFillUpForm, ProfessionalInfoFillUpForm, ConsumerProfileEditForm, \
    ProfessionalProfileEditForm
from models import ConsumerProfile, ProfessionalProfile
from user_helpers import (retrieve_professional_info,
                          get_professional_corresponding_object_by_type_and_lic,
                          get_professional_user)
from utils import *
from django.utils.translation import ugettext_lazy as _
import json


@receiver(user_signed_up)
def set_role_before_sign_up_complete(request, **kwargs):
    user = kwargs.pop('user')
    if 'sociallogin' in kwargs:
        user.role = CONSUMER
    else:
        user.role = request.POST.get('role')
    user.save()


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    """
        Login and redirect
        This is done in order to tackle the situation where user's email retrieved
        from one provider is different from already existing email in the database
        (e.g facebook and google both use same email-id). Specifically, this is done to
        tackle following issues:
        * https://github.com/pennersr/django-allauth/issues/215
    """
    email_address = sociallogin.account.extra_data['email']
    users = get_user_model().objects.filter(email=email_address)
    if users:
        perform_login(request=request, user=users[0], email_verification=settings.ACCOUNT_EMAIL_VERIFICATION)
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL))


@login_required
def sign_up_complete_info(request, **kwargs):
    if request.user.role == CONSUMER:
        if 'success_url' in request.session:
            return redirect(request.session['success_url'])
        else:
            # return redirect('/')
            # return redirect('account_consumer_profile_after_signup')
            return redirect('show_dashboard')
    elif request.user.role == PROFESSIONAL:
        return redirect('account_professional_profile_after_signup')
    else:
        raise UnexpectedMultipleChoice('Unexpected value for user role')
    return HttpResponseServerError


@method_decorator(login_required, name='dispatch')
class DashboardAfterPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return '/'


@method_decorator(login_required, name='dispatch')
class DashboardAfterPasswordSetView(PasswordSetView):
    @property
    def success_url(self):
        return '/'


@method_decorator(login_required, name='dispatch')
class ConsumerProfileAfterSignupView(View):
    # TODO: add a logic, if there is no change, there is no need to save.
    form_class = ConsumerInfoFillUpForm
    template_name = 'consumer_profile_after_signup/consumer_profile_after_signup.html'
    initial = {
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'zipcode': '90024',
        'gender': MALE
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(request)
            # TODO: change redirect to consumer dashboard after implemented
            return redirect(request.path)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfessionalProfileAfterSignupView(View):
    form_class = ProfessionalInfoFillUpForm
    template_name = 'professional_profile_after_signup/professional_profile_after_signup.html'
    # TODO
    initial = {}

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data_to_send = retrieve_professional_info(request)
            if not data_to_send:
                raise Http404(_("Lic number does not exist"))
            return HttpResponse(json.dumps(data_to_send), content_type="application/json")
        else:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(request)
            professional = get_professional_user(request.user)
            # reverse url name with professional type
            business_page_url = reverse(professional.type.lower(), args=[professional.lic_num])
            # print business_page_url
            return redirect(business_page_url)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class ConsumerProfileView(View):
    form_class = ConsumerProfileEditForm
    # TODO: add template
    template_name = 'consumer_profile/consumer_profile.html'
    initial = {}

    # TODO: test for exsiting and not exsiting profile
    def get(self, request, *args, **kwargs):
        # initial form data
        self.initial['first_name'] = request.user.first_name
        self.initial['last_name'] = request.user.last_name
        # profile = request.user.consumer_profiles.first()
        # if not profile:
        #     self.initial['zipcode'] = profile.zipcode
        #     self.initial['gender'] = profile.gender
        # else:
        #     self.
        profile, created = ConsumerProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'zipcode': '90024',
                'gender': MALE
            }
        )
        self.initial['zipcode'] = profile.zipcode
        self.initial['gender'] = profile.gender

        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, _("Your Profile updated."))
            return redirect(request.path)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfessionalProfileView(View):
    form_class = ProfessionalProfileEditForm
    # TODO: add template
    template_name = 'professional_profile/professional_profile.html'
    initial = {}

    # TODO: assume all professional, professional_subtype, profile exsiting,
    # TODO: need validate in the future
    def get(self, request, *args, **kwargs):
        profile = request.user.professional_profiles.first()
        professional = profile.professional
        subtype_list = professional.professional_types.all()
        professional_subtype_list = [item.subtype for item in subtype_list]
        self.initial['license_num'] = professional.lic_num
        self.initial['company_name'] = professional.name
        self.initial['entity_type'] = professional.entity_type
        self.initial['professional_type'] = professional.type
        self.initial['professional_subtype'] = professional_subtype_list
        self.initial['state'] = professional.state
        self.initial['zipcode'] = professional.postal_code
        professional_object = get_professional_corresponding_object_by_type_and_lic(prof_type=professional.type,
                                                                                    lic=professional.lic_num)
        self.initial['street'] = professional_object.street_address

        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # print form.is_valid()
        if form.is_valid():
            # <process form cleaned data>
            form.save(request)

            messages.success(request, _("Your Profile updated."))
            return redirect(request.path)

        return render(request, self.template_name, {'form': form})


class login(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if 'next' in request.path:
            pass
        elif 'HTTP_REFERER' in request.META:
            if not 'accounts/' in request.META['HTTP_REFERER']:
                request.session['success_url'] = request.META['HTTP_REFERER']
        else:
            request.session['success_url'] = '/'
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if 'success_url' in self.request.session:
            success_url = self.request.session['success_url']
        elif 'next' in self.request.path:
            pass
        else:
            success_url = '/'
        try:
            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response
