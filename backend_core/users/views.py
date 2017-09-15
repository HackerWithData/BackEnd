# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from forms import ConsumerInfoFillUpForm, ProfessionalInfoFillUpForm
from utils import *


@login_required
def sign_up_complete_info(request, **kwargs):
    if request.user.role == CONSUMER:
        return render(request, 'before_complete_consumer/before_complete_consumer.html')
        redirect()
    elif request.user.role == PROFESSIONAL:
        return render(request, 'before_complete_professional/before_complete_professional.html')
    else:
        raise UnexpectedMultipleChoice('Unexpected value for user role')


# TODO: test in the morning
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
            # TODO: redirect to home page or user dashboard
            # return redirect('/success/')
            return HttpResponse('success')

        return render(request, self.template_name, {'form': form})


# TODO: test in the morning
@method_decorator(login_required, name='dispatch')
class ProfessionalProfileView(View):

    form_class = ProfessionalInfoFillUpForm
    template_name = 'professional_profile_after_signup/professional_profile_after_signup.html'
    # TODO
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
            # <process form cleaned data>
            form.save(request)
            # TODO: redirect to home page or user dashboard
            return redirect('/success/')

        return render(request, self.template_name, {'form': form})
