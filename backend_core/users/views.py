# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from allauth.account.signals import user_signed_up

from forms import ConsumerInfoFillUpForm, ProfessionalInfoFillUpForm
from user_helpers import retrieve_professional_info
from utils import *

import json

@receiver(user_signed_up)
def set_role_before_sign_up_complete(request, **kwargs):
    user = kwargs.pop('user')
    role = request.POST.get('role')
    user.role = role
    user.save()


@login_required
def sign_up_complete_info(request, **kwargs):
    if request.user.role == CONSUMER:
        return redirect('account_consumer_profile')
    elif request.user.role == PROFESSIONAL:
        return redirect('account_professional_profile')
    else:
        raise UnexpectedMultipleChoice('Unexpected value for user role')
    return HttpResponseServerError


@method_decorator(login_required, name='dispatch')
class ConsumerProfileView(View):

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
            return redirect('home_index')

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfessionalProfileView(View):

    form_class = ProfessionalInfoFillUpForm
    template_name = 'professional_profile_after_signup/professional_profile_after_signup.html'
    # TODO
    initial = {}

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data_to_send = retrieve_professional_info(request)
            print data_to_send
            if not data_to_send:
                raise Http404
            return HttpResponse(json.dumps(data_to_send), content_type="application/json")
        else:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form.save(request)
            # TODO: change redirect to professional dashboard after implemented
            return redirect('home_index')

        return render(request, self.template_name, {'form': form})
